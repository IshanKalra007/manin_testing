# Vynotes Manim Renderer – AWS EC2 Setup Guide

This guide walks you through deploying the Manim renderer on Amazon EC2 so your Vynotes frontend can call it to render math animations.

---

## Prerequisites

- AWS account
- AWS CLI installed and configured (`aws configure`)
- Docker (install locally, or build directly on EC2 – see Step 5 Option B)

---

## Step 1: Create an S3 Bucket

Videos are stored in S3. Create a bucket:

```bash
# Replace with your preferred bucket name (must be globally unique)
export BUCKET_NAME=vynotes-renders-yourname
export AWS_REGION=us-east-1

aws s3 mb s3://$BUCKET_NAME --region $AWS_REGION
```

**Make videos publicly readable** (so the frontend can display them):

```bash
# Create bucket policy for public read
cat > bucket-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::BUCKET_NAME_PLACEHOLDER/*"
    }
  ]
}
EOF

# Replace BUCKET_NAME_PLACEHOLDER with your bucket name in bucket-policy.json
# (On Windows, edit the file manually. On Linux/Mac: sed -i "s/BUCKET_NAME_PLACEHOLDER/$BUCKET_NAME/g" bucket-policy.json)
aws s3api put-bucket-policy --bucket $BUCKET_NAME --policy file://bucket-policy.json
```

**Optional:** Enable CORS if your frontend is on a different domain:

```bash
cat > cors.json << 'EOF'
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "HEAD"],
      "AllowedHeaders": ["*"]
    }
  ]
}
EOF
aws s3api put-bucket-cors --bucket $BUCKET_NAME --cors-configuration file://cors.json
```

---

## Step 2: Create an IAM Role for EC2

The EC2 instance needs permission to write to S3.

1. **Create a role:**
   - AWS Console → IAM → Roles → Create role
   - Trusted entity: **AWS service** → **EC2**
   - Attach policy: **AmazonS3FullAccess** (or a custom policy scoped to your bucket)
   - Name: `VynotesRendererRole`

2. **Or via CLI:**

```bash
# Create trust policy
cat > trust-policy.json << 'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "ec2.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

aws iam create-role --role-name VynotesRendererRole --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name VynotesRendererRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess

# Create instance profile
aws iam create-instance-profile --instance-profile-name VynotesRendererProfile
aws iam add-role-to-instance-profile --instance-profile-name VynotesRendererProfile --role-name VynotesRendererRole
```

---

## Step 3: Launch an EC2 Instance

1. **Launch instance:**
   - AMI: **Ubuntu 22.04 LTS**
   - Instance type: **t3.medium** or **t3.large** (rendering is CPU-heavy)
   - Storage: 20–30 GB
   - IAM role: `VynotesRendererProfile` (from Step 2)
   - Security group: allow inbound **22** (SSH) and **8000** (API)

2. **Or via CLI:**

```bash
# Create security group
aws ec2 create-security-group --group-name vynotes-renderer-sg \
  --description "Vynotes Manim Renderer" --region $AWS_REGION

# Get your IP for SSH (optional, restrict for security)
MY_IP=$(curl -s ifconfig.me)/32

aws ec2 authorize-security-group-ingress --group-name vynotes-renderer-sg \
  --protocol tcp --port 22 --cidr $MY_IP
aws ec2 authorize-security-group-ingress --group-name vynotes-renderer-sg \
  --protocol tcp --port 8000 --cidr 0.0.0.0/0   # Or restrict to your frontend IP

# Launch instance (replace with your subnet, key pair, etc.)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \
  --instance-type t3.medium \
  --key-name YOUR_KEY_PAIR \
  --security-groups vynotes-renderer-sg \
  --iam-instance-profile Name=VynotesRendererProfile \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":30}}]' \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=VynotesRenderer}]'
```

---

## Step 4: Install Docker on EC2

SSH into your instance:

```bash
ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>
```

Install Docker:

```bash
sudo apt-get update
sudo apt-get install -y docker.io
sudo usermod -aG docker ubuntu
# Log out and back in for group to take effect, or:
newgrp docker
```

---

## Step 5: Build and Run the Renderer

**Option A: Build locally and push to ECR (recommended)**

1. Create an ECR repository:

```bash
aws ecr create-repository --repository-name vynotes-manim-renderer --region $AWS_REGION
```

2. Build and push from your machine:

```bash
cd "c:\Users\Hp\PycharmProjects\Manim testing\renderer"
docker build -t vynotes-manim-renderer .
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
docker tag vynotes-manim-renderer:latest YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vynotes-manim-renderer:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vynotes-manim-renderer:latest
```

3. On EC2, pull and run:

```bash
aws ecr get-login-password --region $AWS_REGION | sudo docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
sudo docker pull YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vynotes-manim-renderer:latest

sudo docker run -d \
  --name vynotes-renderer \
  -p 8000:8000 \
  -e S3_BUCKET=$BUCKET_NAME \
  -e AWS_REGION=$AWS_REGION \
  --restart unless-stopped \
  YOUR_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/vynotes-manim-renderer:latest
```

**Option B: Build directly on EC2** (use this if you don't have Docker locally)

1. Zip the `renderer` folder and copy to EC2:

   - **Windows:** Right-click `renderer` → Send to → Compressed folder, then use WinSCP or:
     ```powershell
     scp -i your-key.pem -r "c:\Users\Hp\PycharmProjects\Manim testing\renderer" ubuntu@<EC2_IP>:~/
     ```
   - **Mac/Linux:**
     ```bash
     scp -i your-key.pem -r renderer ubuntu@<EC2_IP>:~/
     ```

2. On EC2:

```bash
cd ~/renderer
sudo docker build -t vynotes-manim-renderer .
sudo docker run -d \
  --name vynotes-renderer \
  -p 8000:8000 \
  -e S3_BUCKET=your-bucket-name \
  -e AWS_REGION=us-east-1 \
  --restart unless-stopped \
  vynotes-manim-renderer:latest
```

---

## Step 6: Verify

```bash
# Health check
curl http://<EC2_PUBLIC_IP>:8000/health

# Test render (simple scene)
curl -X POST http://<EC2_PUBLIC_IP>:8000/render \
  -H "Content-Type: application/json" \
  -d '{
    "code": "from manim import *\n\nclass TestScene(Scene):\n    def construct(self):\n        self.play(Write(Text(\"Hello\")))",
    "scene_name": "TestScene",
    "quality": "ql"
  }'
```

You should get a JSON response with `video_url` pointing to your S3 file.

---

## Step 7: Frontend Integration

Your Vynotes frontend should:

1. Send user math notes to Anthropic → get Manim code.
2. Call the renderer:

```javascript
const response = await fetch('http://<EC2_IP>:8000/render', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    code: manimCodeFromAnthropic,
    scene_name: 'MyScene',  // Extract from AI response
    quality: 'qm'
  })
});
const { video_url } = await response.json();
// Display video_url in a <video> tag
```

---

## Optional: Use a Load Balancer + HTTPS

For production:

1. Put the instance behind an **Application Load Balancer (ALB)**.
2. Add an **HTTPS listener** with an ACM certificate.
3. Point a domain (e.g. `renderer.vynotes.com`) to the ALB.
4. Use `https://renderer.vynotes.com/render` in your frontend.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `S3 upload failed: Access Denied` | Check IAM role has S3 permissions; verify bucket name |
| `Manim failed` | Check container logs: `docker logs vynotes-renderer` |
| Render times out | Use a larger instance (t3.large) or increase timeout in `app.py` |
| CORS errors | Add your frontend origin to CORS config in `app.py` |

---

## Cost Estimate

- **t3.medium**: ~$0.04/hour (~$30/month if always on)
- **S3**: ~$0.023/GB storage + minimal request costs
- Consider **Spot instances** or **auto-scaling** to reduce cost when idle.
