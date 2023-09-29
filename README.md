# BADGER

  

> "badg-er - (verb) to annoy someone by repeatedly asking questions or telling the person to do something"

>

> [**Cambridge Academic Content Dictionary**](https://dictionary.cambridge.org/dictionary/english/ "Cambridge Academic Content Dictionary") © Cambridge University Press

  

> "badger badger badger badger badger badger badger badger badger badger badger badger"

>

> https://www.youtube.com/watch?v=EIyixC9NsLI

  
  

# What does BADGER do?

  
Need to stagger API data requests (such as to fall within a usage quota)? Batch'er! BADGER (**Batch Api-request Data, Get Eventual Results)** is a lightweight dockerized app with a web interface to allow uploading and scheduling API data requests, and downloading related results generated over multiple periods within a single file. BADGER runs persistently in the background, making it ideal for a self-hosted service.

  

If you need to request data spanning multiple periods, it can be a hassle to batch requests and remember to send them in regular intervals before finally collecting results from individual tasks into a single consolidated file. With its focus on data requests, BADGER's web app interface can make it easier to accomplish than writing cron jobs or using more generalized scheduler services.

  

More concretely, in the most basic use case BADGER can be used to automate taking regular data snapshots and have them added to an ongoing file. However, it is primarily designed to handle cases where you may want to send large sets of requests to API's that have limits on the number that can be sent in a period (e.g. a subscription that allows 1,000 / month).

  

Features:

- Uses the `httpx` with `anyio` libraries to facilitate asynchronous requests with rate limiting and retries with exponential backoff

- Summary reports of successes and failures

- Create a calendar event based on expected scheduled completion

- To help with development, includes a test site with configuarable limits to send requests

# Installation
Not yet available

<!--cc/>
With [Docker](https://www.docker.com) installed, run the following command:

    docker run -d kphang/BADGER
-->

# Planned features

- Allow setting up a service to hit an endpoint on another service (such as IFTTT, Zapier) to generate notifications of events (e.g. job completion, task failure, service shutdown)

- Auto-resumption in the event of container shutdown based on a contingency configuration

- Keep track of configurations and limits from previously used API's

- Handling non-data objects