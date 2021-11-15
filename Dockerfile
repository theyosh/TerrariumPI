# Temp small Dockerfile while testing workflow
# docker build -t wkd1/test:workflow-test .
# docker buildx build --platform linux/arm/v7 -t wkd1/test:workflow-test-arm .
FROM alpine:3.14.3
RUN echo "hi" > /test.out
