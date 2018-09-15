import frunner

task_1 = frunner.task('Task 1', 'sleep', '1')
task_2 = frunner.task('Task 2', 'sleep', '1')
task_3 = frunner.task('Task 3', 'python', 'test_task.py')
task_4 = frunner.task('Task 4', 'sleep', '1')
task_A = frunner.task('Task A', 'sleep', '1')
task_2.add_prereq(task_1)
task_3.add_prereq(task_2)
task_4.add_prereq(task_2)
task_3.add_prereq(task_1)

pipeline = frunner.pipeline(schedule="* * * * *")
# all tasks must be added
pipeline.add_tasks(task_1, task_A)
print(pipeline.get_next_run_time())
pipeline.run_immediately()

