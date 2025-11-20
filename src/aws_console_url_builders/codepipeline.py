"""Builder for AWS CodePipeline Console URLs."""

from src.aws_console_url_builders.base import AWSConsoleURLBuilder


class CodePipelineURLBuilder(AWSConsoleURLBuilder):
    """Builder for AWS CodePipeline Console URLs."""

    @classmethod
    def codepipeline_url(cls, region: str, pipeline_name: str) -> str:
        """Build CodePipeline URL."""
        return cls.build_url(
            service="codesuite/codepipeline", region=region, path=f"/pipelines/{pipeline_name}/view"
        )

    @classmethod
    def codepipeline_execution_url(cls, region: str, pipeline_name: str, execution_id: str) -> str:
        """Build CodePipeline execution URL."""
        return cls.build_url(
            service="codesuite/codepipeline",
            region=region,
            path=f"/pipelines/{pipeline_name}/executions/{execution_id}/timeline",
        )
