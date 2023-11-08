# Instructor Notes

## Enroute account used objects

| Object Type | Name           |
| ----------- | -------------- |
| user-group  | de-101-s3      |
| policy      | de-101-rw-s3   |
| user        | de-101-student |

## User Policies

Policy for `student user` (de-101-rw-s3)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadS3All",
      "Effect": "Allow",
      "Action": [
        "s3:ListAllMyBuckets"
      ],
      "Resource": "*"
    },
    {
      "Sid": "ReadS3",
      "Effect": "Allow",
      "Action": [
        "s3:GetObjectAcl",
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": "arn:aws:s3:::de-101-session-6"
    },
    {
      "Sid": "WriteS3",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::de-101-session-6/*"
    }
  ]
}
```

## Additional Notes

- Empty and Delete bucket after practice
- Deactivate user
