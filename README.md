# rahkam
about interview
sudo sysctl fs.inotify.max_user_watches=524288
sudo sysctl fs.inotify.max_user_instances=512

 kind create cluster --name rahkam --config kind-cluster.yml --retain
 kubectl cluster-info --context kind-rahkam


=======================================================================
  kubectl get node -->
     NAME                    STATUS   ROLES           AGE     VERSION
rahkam-control-plane    Ready    control-plane   2m49s   v1.27.3
rahkam-control-plane2   Ready    control-plane   2m18s   v1.27.3
rahkam-control-plane3   Ready    control-plane   68s     v1.27.3
rahkam-worker           Ready    <none>          54s     v1.27.3
rahkam-worker2          Ready    <none>          54s     v1.27.3
rahkam-worker3          Ready    <none>          54s     v1.27.3
=======================================================================

