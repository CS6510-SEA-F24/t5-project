import logging
from typing import List, Optional
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException

from tests.page.element import (
    PipelineElement,
    StageData,
    JobData,
    StagesElement,
    JobsElement,
)
from tests.page.locators import PipelinePageLocators


@dataclass
class PipelineData:
    """Complete pipeline data structure"""

    name: str
    stages: List[StageData]
    all_artifacts: List[str]


@dataclass
class VerificationResult:
    """Result of pipeline verification"""

    success: bool
    message: Optional[str] = None


class PipelineError(Exception):
    """Custom exception for pipeline operations"""

    pass


class BasePage:
    """Base class for all pages"""

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(__name__)


class PipelinePage(BasePage):
    """Pipeline page with business logic"""

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.pipeline_element = PipelineElement(driver)
        self.stages_element = StagesElement(driver)
        self.jobs_element = JobsElement(driver)
        self._pipeline_data = None

    def get_pipeline_data(self) -> Optional[PipelineData]:
        """Get complete pipeline data"""
        if not self._pipeline_data:
            try:
                name = self.get_pipeline_name()
                self.logger.info(f"Pipeline name: {name}")
                if not name:
                    self.logger.error("Failed to get pipeline name")
                    return None

                stages = self._get_stages_data()
                self.logger.info(f"Got {len(stages)} stages")

                all_artifacts = self._get_all_artifacts()
                self.logger.info(f"Got {len(all_artifacts)} artifacts")

                self._pipeline_data = PipelineData(
                    name=name, stages=stages, all_artifacts=all_artifacts
                )
            except WebDriverException as e:
                self.logger.error(f"Failed to get pipeline data: {str(e)}")
                return None
            except Exception as e:
                self.logger.error(f"Unexpected error: {str(e)}")
                return None

        return self._pipeline_data

    def get_pipeline_name(self) -> Optional[str]:
        """Get pipeline name"""
        name = self.pipeline_element.get_title()
        if not name:
            self.logger.error("Failed to get pipeline name from element")
            return None
        self.logger.info(f"Successfully got pipeline name: {name}")
        return name

    def get_stages(self) -> List[str]:
        """Get all stage names"""
        return self.stages_element.get_stages()

    def get_stage_artifacts(self, stage_name: str) -> List[str]:
        """Get artifacts for a specific stage"""
        try:
            locator = PipelinePageLocators.stage_artifacts(stage_name)
            if not locator:
                return []
            xpath = (
                f"//div[contains(@class, 'artifacts-title')]"
                f"[contains(text(), '{stage_name} Artifacts')]"
                f"/following-sibling::ul[@class='artifacts-list']/li"
            )
            stage_artifacts_box = self.driver.find_elements(By.XPATH, xpath)
            artifacts = [art.text.strip() for art in stage_artifacts_box if art.text]
            self.logger.info(f"Found {len(artifacts)} artifacts for stage {stage_name}")
            return artifacts
        except WebDriverException as e:
            self.logger.error(f"Failed to get stage artifacts: {str(e)}")
            return []

    def get_job_dependencies(self, job_id: str) -> List[str]:
        """Get dependencies for a specific job"""
        try:
            job_element = self.driver.find_element(By.ID, f"job_{job_id}")
            needs_str = job_element.get_attribute("data-needs")
            return needs_str.split(",") if needs_str and needs_str.strip() else []
        except Exception as e:
            self.logger.error(f"Failed to get dependencies for job {job_id}: {str(e)}")
            return []

    def is_job_allow_failure(self, job_id: str) -> bool:
        """Check if job allows failure"""
        try:
            job_element = self.driver.find_element(By.ID, f"job_{job_id}")
            allow_failure = job_element.get_attribute("data-allow-failure")
            return allow_failure.lower() == "true" if allow_failure else False
        except Exception as e:
            self.logger.error(
                f"Failed to check allow_failure for job {job_id}: {str(e)}"
            )
            return False

    def verify_pipeline_structure(self) -> VerificationResult:
        """Verify complete pipeline structure"""
        pipeline_data = self.get_pipeline_data()
        if not pipeline_data:
            return VerificationResult(False, "Failed to get pipeline data")

        try:
            if not pipeline_data.stages:
                return VerificationResult(False, "No stages found")

            for stage in pipeline_data.stages:
                if not self._verify_stage_data(stage):
                    return VerificationResult(False, f"Invalid stage: {stage.name}")

            return VerificationResult(True, "Pipeline verification successful")
        except Exception as e:
            self.logger.error(f"Pipeline verification failed: {str(e)}")
            return VerificationResult(False, str(e))

    def _get_stages_data(self) -> List[StageData]:
        """Get data for all stages"""
        stages = []
        for stage_name in self.get_stages():
            jobs = self._get_stage_jobs(stage_name)
            artifacts = self.get_stage_artifacts(stage_name)
            stages.append(StageData(name=stage_name, jobs=jobs, artifacts=artifacts))
        return stages

    def _get_stage_jobs(self, stage_name: str) -> List[JobData]:
        """Get all jobs in a stage"""
        try:
            jobs = []
            stage_jobs = self.jobs_element.get_stage_jobs(stage_name)

            for job in stage_jobs:
                job_id = job.get_attribute("id").replace("job_", "")
                job_data = self.jobs_element.get_job_data(job_id)
                if job_data:
                    jobs.append(job_data)

            self.logger.info(f"Found {len(jobs)} jobs in stage {stage_name}")
            return jobs
        except Exception as e:
            self.logger.error(f"Failed to get jobs for stage {stage_name}: {str(e)}")
            return []

    def _verify_stage_data(self, stage: StageData) -> bool:

        # 1. Verify stage name
        if not stage.name:
            self.logger.error("Stage name is missing")
            return False
        # 2. Get stage jobs and artifact
        stage_jobs = self.jobs_element.get_stage_jobs(stage.name)
        stage_artifacts = self.stages_element.get_stage_artifacts(stage.name)

        # 3. Verify jobs data if exists
        if stage_jobs:
            for job in stage_jobs:
                job_name = job.get_attribute("data-job-name")
                if not job_name:
                    self.logger.error(f"Job in stage {stage.name} has missing name")
                    return False

                job_stage = job.get_attribute("data-stage")
                if job_stage != stage.name:
                    self.logger.error(
                        f"Job {job_name} has incorrect stage assignment: "
                        f"expected {stage.name}, got {job_stage}"
                    )
                    return False
        # 4. Verify artifacts match with jobs
        if stage_artifacts:
            job_artifacts = []
            for job in stage_jobs:
                job_artifacts_elem = job.find_elements(By.CLASS_NAME, "job-artifact")
                job_artifacts.extend([art.text.strip() for art in job_artifacts_elem])

            for artifact in stage_artifacts:
                if artifact not in job_artifacts:
                    self.logger.error(
                        f"Stage {stage.name} has artifact '{artifact}' "
                        f"not declared in any job"
                    )
                    return False
        return True

    def _get_all_artifacts(self) -> List[str]:
        """Get all artifacts from all stages"""
        all_artifacts = []
        try:
            for stage_name in self.get_stages():
                stage_artifacts = self.get_stage_artifacts(stage_name)
                all_artifacts.extend(stage_artifacts)
            return all_artifacts
        except Exception as e:
            self.logger.error(f"Failed to get all artifacts: {str(e)}")
            return []
