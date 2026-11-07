from app.modules.professional_services.kubernetes.models import (
    KubernetesCluster,
    KubernetesDeployment,
    KubernetesMaintenance,
    KubernetesMigration,
    KubernetesNamespace,
    KubernetesNode,
    KubernetesWorkload,
)
from app.modules.professional_services.kubernetes.schemas import (
    KubernetesClusterCreate,
    KubernetesClusterRead,
    KubernetesDeploymentCreate,
    KubernetesDeploymentRead,
    KubernetesMaintenanceCreate,
    KubernetesMaintenanceRead,
    KubernetesMigrationCreate,
    KubernetesMigrationRead,
    KubernetesNamespaceCreate,
    KubernetesNamespaceRead,
    KubernetesNodeCreate,
    KubernetesNodeRead,
    KubernetesWorkloadCreate,
    KubernetesWorkloadRead,
)

RESOURCES = {
    "clusters": (KubernetesCluster, KubernetesClusterCreate, KubernetesClusterRead, {}),
    "nodes": (
        KubernetesNode,
        KubernetesNodeCreate,
        KubernetesNodeRead,
        {"cluster_id": KubernetesCluster},
    ),
    "namespaces": (
        KubernetesNamespace,
        KubernetesNamespaceCreate,
        KubernetesNamespaceRead,
        {"cluster_id": KubernetesCluster},
    ),
    "workloads": (
        KubernetesWorkload,
        KubernetesWorkloadCreate,
        KubernetesWorkloadRead,
        {
            "cluster_id": KubernetesCluster,
            "namespace_id": (KubernetesNamespace, "cluster_id", "cluster_id"),
        },
    ),
    "deployments": (
        KubernetesDeployment,
        KubernetesDeploymentCreate,
        KubernetesDeploymentRead,
        {
            "cluster_id": KubernetesCluster,
            "workload_id": (KubernetesWorkload, "cluster_id", "cluster_id"),
            "namespace_id": (KubernetesNamespace, "cluster_id", "cluster_id"),
        },
    ),
    "migrations": (
        KubernetesMigration,
        KubernetesMigrationCreate,
        KubernetesMigrationRead,
        {"target_cluster_id": KubernetesCluster},
    ),
    "maintenance": (
        KubernetesMaintenance,
        KubernetesMaintenanceCreate,
        KubernetesMaintenanceRead,
        {"cluster_id": KubernetesCluster},
    ),
}