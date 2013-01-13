from . import dependency
from .exceptions import InvalidCommand
from .cmd_base import DoitCmdBase, subtasks_iter


class Forget(DoitCmdBase):
    doc_purpose = "clear successful run status from internal DB"
    doc_usage = "[TASK ...]"
    doc_description = None

    cmd_options = ()

    def _execute(self):
        """remove saved data successful runs from DB
        """
        dependency_manager = dependency.Dependency(self.dep_file)

        # no task specified. forget all
        if not self.sel_tasks:
            dependency_manager.remove_all()
            self.outstream.write("forgeting all tasks\n")

        # forget tasks from list
        else:
            tasks = dict([(t.name, t) for t in self.task_list])
            for task_name in self.sel_tasks:

                # check task exist
                if task_name not in tasks:
                    msg = "'%s' is not a task."
                    raise InvalidCommand(msg % task_name)

                # for group tasks also remove all tasks from group
                sub_list = [t.name for t in subtasks_iter(tasks,
                                                          tasks[task_name])]
                for to_forget in [task_name] + sub_list:
                    # forget it - remove from dependency file
                    dependency_manager.remove(to_forget)
                    self.outstream.write("forgeting %s\n" % to_forget)

        dependency_manager.close()