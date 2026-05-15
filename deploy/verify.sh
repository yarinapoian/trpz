#!/bin/bash
set -e

DEPLOY_HOST=${1:-localhost}
TIMEOUT=${2:-30}
ELAPSED=0

echo "Verifying deployment"

while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  if curl -sf "http://${DEPLOY_HOST}/health/alive" > /dev/null 2>&1; then
    echo "Health alive endpoint is responding"

    if curl -sf "http://${DEPLOY_HOST}/health/ready" > /dev/null 2>&1; then
      echo "Health ready endpoint is responding"
      echo "Application is ready"
      exit 0
    else
      echo "Health ready endpoint is not responding yet"
    fi
  else
    echo "Application not responding yet"
  fi

  sleep 2
  ELAPSED=$((ELAPSED + 2))
done

echo "Verification failed - application did not become ready"
exit 1