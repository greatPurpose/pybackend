#!/usr/bin/env bash
kubectl config set-context --current --namespace=$ENVIRONMENT

if [[ "$CI_COMMIT_TAG" != "" ]]; then
  export IMAGE_TAG=$CI_COMMIT_TAG
fi

export DATE=$(date +%s)

envsubst < configmap.$ENVIRONMENT.yml > k8s-configmap.yml && kubectl apply -f k8s-configmap.yml
envsubst < main.yml > k8s-main.yml && kubectl apply -f k8s-main.yml

if [[ $? != 0 ]]; then exit 1; fi

kubectl rollout status deployments/$CI_PROJECT_NAME

if [[ $? != 0 ]]; then
    kubectl logs $(kubectl get pods --sort-by=.metadata.creationTimestamp | grep "$CI_PROJECT_NAME" | awk '{print $1}' | tac | head -1 ) --tail=20 && exit 1;
fi
