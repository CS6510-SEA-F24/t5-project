
# Week 7

# Completed tasks 

| Task                                                                | Weight | 
|---------------------------------------------------------------------|--------| 
| Show arrow from Job dependencies                                    | 1      |
| Represent a pipeline configuration file as a graphic in HTML format | 3      | 
| Add GRP_design_doc.md and Graphical Representation Tool Selection document   | 1      |
| Add CI workflow for GitHub Actions                                    | 1      |

> Good throughput this week. Keep it up! 

# Carry over tasks 

| Task                                     | Weight | Assignee |
|------------------------------------------|--------|----------|  
| Use Selenium library to handle html page | 1      | Yuanyuan | 
| Weekly Report 7                          | 1      | Yuanyuan |

# New tasks 

| Task | Weight | Assignee |
| ---- |-------|----------|

# What worked this week? 
- Visualizing Pipeline Configuration Files as HTML Graphics:
  - The YAML format pipeline configuration files were successfully converted into a visual HTML representation. Utilizing a templating engine, structured HTML was dynamically generated to include all stages and jobs, significantly enhancing the readability and maintainability of the pipeline.
- Displaying Job Dependency Arrows:
  - A feature was implemented to dynamically draw arrows between jobs on the webpage, representing their dependencies. By leveraging the DOMContentLoaded event in JavaScript, arrows are drawn once the page is fully loaded, thereby improving the user's comprehension of job relationships.
- Adding CI Workflow for GitHub Actions:
  - A CI workflow was successfully established using GitHub Actions, which automatically executes tests and builds with each code commit. This setup has notably improved code quality and delivery efficiency.
- Adding GRP_design_doc.md and Documentation for Graphical Representation Tool Selection:
  - I wrote and added the GRP_design_doc.md document, which details the design concepts and implementation specifics of the project. Additionally, I selected suitable graphical representation tools and documented them for team reference.



# What did not work this week? 
- NA

# Design updates 
- Graphical Representation Tool Selection（https://github.com/CS6510-SEA-F24/t5-project/blob/ec26660b53255b8e002842cd63aff49a4115a4dd/dev-docs/design_doc/Graphical%20_Representation%20_Tool%20Selection.md）
- Graphical Representation of Pipelines (GRP)Design Document（https://github.com/CS6510-SEA-F24/t5-project/blob/ec26660b53255b8e002842cd63aff49a4115a4dd/dev-docs/design_doc/GRP_design_doc.md）
- Graphical Representation of Pipelines Design Doc(https://docs.google.com/document/d/1EBjUZghnbNYWNWvdYkpaDX_hCFstS53lY5C7ZLWqFdU/edit?usp=sharing)
- GitLab pipeline (https://docs.gitlab.com/ee/ci/pipelines/)


> Let's get the testing of the output with Selenium up and running and then we can talk about 
> some more features to add to the tool. 