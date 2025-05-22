variable "credentials" {
  description = "My Credentials"
  default     = "./key/dtc-de-course-460512-e3d58a03a3eb.json"
}

variable "project" {
  description = "Project"
  default     = "dtc-de-course-460512"
}

variable "region" {
  description = "Region"
  default     = "europe-west10"
}

variable "location" {
  description = "Project Location"
  default     = "EU"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "de_bootcamp_bq"
}

variable "gcs_bucket_name" {
  description = "My Storage Bucket Name"
  default     = "de-bootcamp-bucket"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}