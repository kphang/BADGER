# App

Design principles:
- Breadcrumb approach

## /
Main page shows notifications and active jobs and summaries

Links to:
- View All Notifications
- Create Job
- View All Jobs

**/createjob** Job Creation
- General job data
- Configuration
- Upload requests
- Confirm request field
- View requests data
- Test one request
- Run now () - check for available limit for period
- Save and schedule


### /job (View All Jobs)
Shows table of all jobs and summaries

**/job/{jobId}** Job Details
- Shows job details (configuration)
- Edit configuration
- Edit requests (add or remove rows)
- Shows list of batches associated with job
- Shows list of requests associted with job (and current status)
- Download button
- Run now option 

**/job/{jobId}/batch/{batchId}** Batch Details


**/job/{jobId}/request/{requestId}** Request and Response Details
- Shows request details and successful response details (if available)
- Shows table of failed requests

### /notification (View All Notifications)





# Objects

## Job

### Batch Config
Need to figure out how it gets overwritten based on experience
Need to allow for both experimental and fixed (for cases where rates might be known)
Need to handle inputting multiple rates

## Batch


## Request


## Notifications

Should Responses be a separate object? The would mean that every Request can have multiple Responses. Each Response is associated with a single batch (in contrast a request can be associated with multiple batches)


# Asynchronicity
Maybe we can do a linear growth of concurrent requests to identify max concurrency separate from rate limiting.