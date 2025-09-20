import { S3Client, GetObjectCommand, PutObjectCommand, HeadObjectCommand, DeleteObjectCommand } from '@aws-sdk/client-s3';
import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import type {StorageService} from '@/core/ports/interfaces'
import {env} from "@/env"


export class R2StorageService implements StorageService {
  private s3Client: S3Client;

  constructor() {
    this.s3Client = new S3Client({
      region: env.R2_REGION,
      endpoint: env.R2_ENDPOINT_URL,
      credentials: {
        accessKeyId: env.R2_ACCESS_KEY_ID,
        secretAccessKey: env.R2_SECRET_ACCESS_KEY,
      },
      forcePathStyle: true,
    });
  }

  async getPresignedUrl(key: string): Promise<string> {
    // If using custom domain, construct URL directly
    if (env.R2_CUSTOM_DOMAIN) {
      return `${env.R2_CUSTOM_DOMAIN}/${key}`;
    }

    // Otherwise generate presigned URL
    const command = new GetObjectCommand({
      Bucket: env.R2_BUCKET_NAME,
      Key: key,
    });

    return await getSignedUrl(this.s3Client, command, { expiresIn: 3600 });
  }

  async uploadFile(file: Buffer, key: string, contentType: string): Promise<string> {
    const command = new PutObjectCommand({
      Bucket: env.R2_BUCKET_NAME,
      Key: key,
      Body: file,
      ContentType: contentType,
    });

    await this.s3Client.send(command);
    return key;
  }

  async fileExists(key: string): Promise<boolean> {
    try {
      const command = new HeadObjectCommand({
        Bucket: env.R2_BUCKET_NAME,
        Key: key,
      });
      await this.s3Client.send(command);
      return true;
    } catch (error) {
      return false;
    }
  }

  async deleteFile(key: string): Promise<void> {
    const command = new DeleteObjectCommand({
      Bucket: env.R2_BUCKET_NAME,
      Key: key,
    });
    
    await this.s3Client.send(command);
  }
}
