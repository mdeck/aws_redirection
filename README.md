# aws_redirection

This allows two web servers to serve one domain, via fail-over.  Incoming requests that normally would respond with a 403/404 on the first server are redirected to the second server.

1. Start with your first server setup as a first distribution on AWS CloudFront.

2. Setup a second distribution to redirect to the second server, via a lambda@edge function.
    - Create a second distribution with any origin (I used a random S3 bucket), with an origin ID of "dummy-origin".
    - Edit the default cache behavior for this distribution.  Associate this lambda@edge function with Origin Request events.  You don't need to include the body.
    - Now you have something like alskdjfksdksdj.cloudfront.net which will always redirect to the domain that is hardcoded into the lambda function.  Here, I have it set to redirect to "z.k2photo.gallery".

3. Edit the first distribution to fail-over to your second distribution.
    - Add a second Origin, pointed to your alskdjfksdksdj.cloudfront.net (second distribution address).  Give it an origin ID of "always-redirect".  This can be set to HTTP only, as it's internal to AWS.
    - Create a new Origin Group, and add both your Origins.  "always-redirect" should be the second item.
    - Select which HTTP errors you want to fail-over redirect.
    - Give it an Origin Group ID of "redirect-on-error".

That's it!  Now whenever a request to the original server fails, the request will fail-over to your redirection lambda.  CloudFront will also cache redirection responses iaw the cache behavior policy set in the second distribution.
