# Process stuffs
pv = {}  # Process variable container storage
pvn = {}  # Process names list
pvd = {}  # Process control data
pid_seq = -1  # PID sequence number. No need for advanced logic here.
pid_act = []  # Active process list
# It's a stack effectively, since we are operating on one thread.


class Unset:  # None 2.0
    pass


# Backend functions
def pid_alloc(pr_name: str, owner: str, resume: bool) -> int:
    # Allocate a pid and variable storage for that process.
    global pid_seq, pid_act
    if resume and pr_name in pvn:
        res = pvn[pr_name]
        return res
    # Fall through otherwise
    pid_seq += 1
    pv[pid_seq] = {}
    pvd[pid_seq] = []
    pvd[pid_seq].append(pr_name)  # id 0, name.
    pvd[pid_seq].append(resume)  # id 1, resumable task.
    pvd[pid_seq].append(owner)  # id 2, owner name.
    pvd[pid_seq].append(1)  # id 3, status, 0 Active, 1 Sleep, 2 Zombie.
    pvn[pr_name] = pid_seq
    return pid_seq


def pid_free(pid: int) -> bool:
    # End a task and wipe it's memory, returns False when stuff was tampered with.
    res = True
    if pid in pv:
        if not pvd[pid][1]:
            pvn.pop(pvd[pid][0])
            pvd.pop(pid)
            pv.pop(pid)
        else:
            pvd[pid][3] = 1
    else:
        res = False
    return res


def pid_activate(pid: int) -> bool:
    # Add pid in list of active pids.
    if pid in pv and pid not in pid_act:
        pid_act.append(pid)
        pvd[pid][3] = 0
        return True
    else:
        return False


def pid_deactivate() -> None:
    # Removes active pid from pid list.
    pid_act.pop()


# Frontend functions
def get_pid() -> int:
    # Get current active pid
    return pid_act[-1]


def get_parent_pid() -> int:
    # Get parent pid
    return pid_act[-2]


def backtrack_to_process(pid: int) -> None:
    if get_pid() == pid:
        return
    if pid in pid_act:
        while get_pid() != pid:
            end_process()
    else:
        pid_activate(pid)


def vr(varn: str, dat=Unset, pid: int = None):
    """
    Set / Get a variable in container storage.

    You can safely pass None to be set as a value.
    """
    res = None
    if pid is None:
        pid = get_pid()
    if dat is Unset:
        # print(f"GET [{pid}][{varn}]")
        res = pv[pid][varn]
    else:
        # print(f"SET [{pid}][{varn}] = {dat}")
        pv[pid][varn] = dat
    return res


def vra(varn: str, dat, pid: int = None) -> None:
    """
    Variable append.
    Append to a variable in container storage.

    You can safely pass None to be appended.
    """
    if pid is None:
        pid = get_pid()
    # print(f"APPEND [{pid}][{varn}] + {dat}")
    pv[pid][varn].append(dat)


def vrp(varn: str, dat=1, pid: int = None) -> None:
    """
    Variable plus.
    Add something to a variable in container storage.

    Adds 1 by default.
    """
    if pid is None:
        pid = get_pid()
    # print(f"ADD [{pid}][{varn}] + {dat}")
    pv[pid][varn] += dat


def vrm(varn: str, dat=1, pid: int = None) -> None:
    """
    Variable minus.
    Subtract something to a variable in container storage.

    Subtracts 1 by default.
    """
    if pid is None:
        pid = get_pid()
    # print(f"SUB [{pid}][{varn}] - {dat}")
    pv[pid][varn] -= dat


def vrd(varn: str, pid: int = None) -> None:
    """
    Variable delete.

    Delete a variable from container storage.
    """
    if pid is None:
        pid = get_pid()
    # print(f"DEL [{pid}][{variable_name}]")
    del pv[pid][varn]


def launch_process(pr_name: str, owner: str = "Nobody", resume: bool = False) -> int:
    # Get a pid, and activate it immediately.
    if not resume:
        pr_name_og = pr_name
        pr_name_inc = 1
        while pr_name in pvn:
            pr_name = pr_name_og + str(pr_name_inc)
            pr_name_inc += 1
    tmppid = pid_alloc(pr_name, owner=owner, resume=resume)
    pid_activate(tmppid)
    # print("Launched process:", pr_name, tmppid)
    return tmppid


def rename_process(pr_name: str) -> None:
    # Rename current process to target name.
    if pr_name != pvd[get_pid()][0]:
        pr_name_og = pr_name
        pr_name_inc = 1
        while pr_name in pvn:
            pr_name = pr_name_og + str(pr_name_inc)
            pr_name_inc += 1
        pvn.pop(pvd[get_pid()][0])
        pvn[pr_name] = get_pid()
        pvd[get_pid()][0] = pr_name
        # print("Renamed process:", pr_name, get_pid())


def end_process() -> None:
    # End current process.
    # print("End process:", pvd[get_pid()][0], get_pid())
    pid_free(get_pid())
    pid_deactivate()


def clear_process_storage() -> None:
    pv.pop(get_pid())
    pv[get_pid()] = {}
