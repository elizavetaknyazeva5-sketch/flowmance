# run_workflow.py
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import json
import os
from app.core.database import engine
from app.db import models
from app.services.workflow_manager import run_workflow

def ensure_demo():
    models.Base.metadata.create_all(bind=engine)
    with Session(engine) as s:
        user = s.query(models.User).first()
        if not user:
            user = models.User(username="demo", password_hash="demo")
            s.add(user); s.commit(); s.refresh(user)
        proj = s.query(models.Project).filter(models.Project.owner_id == user.id).first()
        if not proj:
            proj = models.Project(owner_id=user.id, name="Demo")
            s.add(proj); s.commit(); s.refresh(proj)
        wf = models.Workflow(project_id=proj.id, name="Create landing demo")
        s.add(wf); s.commit(); s.refresh(wf)
        s.add(models.WorkflowStep(workflow_id=wf.id, order=1, agent_name="MarketResearchAgent", params=json.dumps({"market":"B2B"})))
        s.add(models.WorkflowStep(workflow_id=wf.id, order=2, agent_name="ContentAgent", params=json.dumps({"content_topic":"лендинг"})))
        s.add(models.WorkflowStep(workflow_id=wf.id, order=3, agent_name="AICopywriter", params=json.dumps({"topic":"лендинг"})))
        s.commit()
        return wf.id

if __name__ == "__main__":
    wf_id = ensure_demo()
    with Session(engine) as s:
        res = run_workflow(s, wf_id)
        print(res)
