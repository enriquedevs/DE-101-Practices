# Instructor Notes

## Enroute account used objects

| Object Type | Name           |
| ----------- | -------------- |
| user-group  | de-101-s3      |
| policy      | de-101-rw-s3   |
| user        | de-101-student |

## User Policies

* Add permissions to handle bucket to students

>Policy for role `de-101-external-s3-db` (de-101-rw-s3)

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
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:GetObjectAcl"
      ],
      "Resource": ["arn:aws:s3:::de-101-session-6*", "arn:aws:s3:::de-101-session-12*"]
    },
    {
      "Sid": "WriteS3",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": ["arn:aws:s3:::de-101-session-6/*", "arn:aws:s3:::de-101-session-12/*"]
    }
  ]
}
```

## Additional Notes

* Bucket must be public
* Run generator beforehand \
  `python3 generator.py --hdfs -y 2019 -r 3 -c toyota yamaha ferrari mazda`
* Upload folder \
  `aws s3 sync generated_data s3://de-101-session-12/generated_data/ --profile enroute-jesus_gaona`
