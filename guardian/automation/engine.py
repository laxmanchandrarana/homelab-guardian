from datetime import datetime

from guardian.automation.storage import get_connection
from guardian.automation.actions import *

class AutomationEngine:

    def get_rules(self):

        conn = get_connection()

        rows = conn.execute(
            "SELECT * FROM automation_rules WHERE enabled=1 ORDER BY priority"
        ).fetchall()

        conn.close()

        return rows

    def create_job(self, rule):

        conn = get_connection()

        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO automation_jobs
            (
                rule_id,
                service,
                status,
                progress,
                started_at
            )
            VALUES(?,?,?,?,?)
            """,
            (
                rule["id"],
                rule["target"],
                "running",
                0,
                datetime.utcnow().isoformat(),
            ),
        )

        conn.commit()

        job = cur.lastrowid

        conn.close()

        return job

    def update_progress(self, job, progress, status=None):

        conn = get_connection()

        if status:

            conn.execute(
                """
                UPDATE automation_jobs
                SET progress=?,status=?
                WHERE id=?
                """,
                (
                    progress,
                    status,
                    job,
                ),
            )

        else:

            conn.execute(
                """
                UPDATE automation_jobs
                SET progress=?
                WHERE id=?
                """,
                (
                    progress,
                    job,
                ),
            )

        conn.commit()

        conn.close()

    def log(self, job, level, message):

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO automation_logs
            (
                job_id,
                timestamp,
                level,
                message
            )
            VALUES(?,?,?,?)
            """,
            (
                job,
                datetime.utcnow().isoformat(),
                level,
                message,
            ),
        )

        conn.commit()

        conn.close()

    def execute(self, rule):

        job = self.create_job(rule)

        self.update_progress(job, 10)

        self.log(job, "INFO", "Automation started")

        if rule["action"] == "restart_container":

            result = restart_container(rule["target"])

        elif rule["action"] == "stop_container":

            result = stop_container(rule["target"])

        elif rule["action"] == "start_container":

            result = start_container(rule["target"])

        elif rule["action"] == "restart_service":

            result = restart_service(rule["target"])

        else:

            result = {
                "success": False,
                "stderr": "Unsupported action",
            }

        self.update_progress(job, 80)

        if result["success"]:

            self.log(job, "INFO", result.get("stdout", ""))

            self.update_progress(job, 100, "completed")

        else:

            self.log(job, "ERROR", result.get("stderr", ""))

            self.update_progress(job, 100, "failed")

        return result

engine = AutomationEngine()
