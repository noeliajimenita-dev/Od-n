from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class OdinOracleCloudConfig:
    region: str = ""
    availability_domain: str = ""
    compartment_ocid: str = ""
    instance_ocid: str = ""
    ssh_user: str = "odin"
    deployment_path: str = "/opt/odin"
    service_name: str = "odin"

    @classmethod
    def from_environment(cls) -> "OdinOracleCloudConfig":
        return cls(
            region=os.getenv("OCI_REGION", ""),
            availability_domain=os.getenv(
                "OCI_AVAILABILITY_DOMAIN",
                "",
            ),
            compartment_ocid=os.getenv(
                "OCI_COMPARTMENT_OCID",
                "",
            ),
            instance_ocid=os.getenv(
                "OCI_INSTANCE_OCID",
                "",
            ),
            ssh_user=os.getenv(
                "ODIN_SSH_USER",
                "odin",
            ),
            deployment_path=os.getenv(
                "ODIN_DEPLOYMENT_PATH",
                "/opt/odin",
            ),
            service_name=os.getenv(
                "ODIN_SERVICE_NAME",
                "odin",
            ),
        )

    def validate(self) -> list[str]:
        errors: list[str] = []

        if not self.region.strip():
            errors.append("OCI_REGION is required")

        if not self.compartment_ocid.strip():
            errors.append("OCI_COMPARTMENT_OCID is required")

        if not self.instance_ocid.strip():
            errors.append("OCI_INSTANCE_OCID is required")

        if not self.ssh_user.strip():
            errors.append("ODIN_SSH_USER cannot be empty")

        if not self.deployment_path.strip():
            errors.append("ODIN_DEPLOYMENT_PATH cannot be empty")

        if not self.service_name.strip():
            errors.append("ODIN_SERVICE_NAME cannot be empty")

        return errors

    def is_valid(self) -> bool:
        return not self.validate()

    def to_dict(self) -> dict[str, str]:
        return {
            "region": self.region,
            "availability_domain": self.availability_domain,
            "compartment_ocid": self.compartment_ocid,
            "instance_ocid": self.instance_ocid,
            "ssh_user": self.ssh_user,
            "deployment_path": self.deployment_path,
            "service_name": self.service_name,
              }
