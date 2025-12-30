# 🚦 操作系统第3章：进程描述和控制 (Process Description and Control)

## 🌟 核心逻辑：为什么要有“进程”？

程序（Program）只是躺在硬盘上的死代码。为了让计算机能同时干多件事（比如一边听歌一边写文档），OS 必须把这些代码“跑”起来，并且在它们之间快速切换。

进程 (Process) 就是“跑起来的程序”。这一章就在讲 OS 怎么管理这些跑来跑去的东西。

## 第一部分：什么是进程 (What is a Process?)

*对应课件 Page 4-9*

### 1. 核心定义

- **进程 (Process)**：
  - **A program in execution** (正在执行中的程序)。
  - **An instance of a program** (程序的一个实例)。
  - **The entity that can be assigned to and executed on a processor** (能被分配给CPU执行的实体)。
- **进程 vs 程序**：
  - **程序**：静态的（书）。
  - **进程**：动态的（读书这个动作）。

### 2. 进程的组成 (Process Elements)

一个进程主要由三部分组成：

1. **程序代码 (Program Code)**：可能被多个进程共享（比如大家都开了Word）。
2. **数据集 (Set of Data)**：属于这个进程的变量、工作区。
3. **进程控制块 (PCB - Process Control Block)**：**最重要的数据结构！**
   - 它是OS用来管理进程的“身份证”或“档案”。
   - 包含了进程ID、状态、优先级、寄存器值等。

## 第二部分：进程状态 (Process States) 🔥🔥 必考核心

*对应课件 Page 10-28*

OS 通过改变进程的状态来调度它们。你要能默写出**五状态模型**和**七状态模型**。

### 1. 轨迹 (Trace)

- 进程执行指令的序列。
- **Dispatcher (分派器)**：OS中负责把CPU切换给不同进程的小程序。

### 2. 两状态模型 (Two-State)

- **Running** (正在跑) vs **Not-Running** (没在跑)。
- 缺点：Not-Running 的进程里，有的准备好了，有的还在等I/O，混在一起效率低。

### 3. 五状态模型 (Five-State Model) —— 重点背诵

- **New (新建)**：进程刚被创建，还没进内存。
- **Ready (就绪)**：**万事俱备，只欠CPU**。只要给它CPU，马上就能跑。
- **Running (运行)**：正在CPU上跑。
- **Blocked / Waiting (阻塞/等待)**：**在等某件事发生**（比如等I/O读完，等键盘输入）。给它CPU它也跑不了。
- **Exit (退出)**：跑完了或出错了，正在被收拾。

**关键转换 (Transitions)**：

- **Running -> Ready**：**超时 (Time-out)**。时间片用完了，被OS强行剥夺CPU，乖乖回去排队。
- **Running -> Blocked**：**等待事件 (Event Wait)**。进程自己请求I/O，主动让出CPU。
- **Blocked -> Ready**：**事件发生 (Event Occurs)**。I/O做完了，进程从“等”变成“准备好”。

### 4. 挂起进程 (Suspended Processes) —— 难点

- **问题**：内存满了怎么办？
- **解决**：**交换 (Swapping)**。把内存里暂时不能跑（Blocked）或者优先级低的进程，整个踢到硬盘（Disk）上去。
- **Suspended (挂起)**：进程被踢到了硬盘上。
- **引入挂起后的七状态模型**：
  - **Blocked/Suspend**：在硬盘上等I/O。
  - **Ready/Suspend**：在硬盘上，但已经准备好跑了（只要OS把它读回内存）。

## 第三部分：进程描述 (Process Description)

*对应课件 Page 29-47*

OS 怎么在底层管理这些进程？

### 1. OS 的控制表 (Control Tables)

OS 维护四种表来知晓天下事：

- **Memory Tables** (内存表)
- **I/O Tables** (I/O表)
- **File Tables** (文件表)
- **Process Tables** (进程表)

### 2. 进程映像 (Process Image)

进程在内存里的样子，包含四块：

1. **User Program** (代码)
2. **User Data** (数据)
3. **Stack** (栈)：用来保存函数调用、参数。**LIFO (后进先出)**。
4. **PCB** (进程控制块)。

### 3. PCB 里到底有什么？ (PCB Elements)

分为三类信息：

1. **进程标识 (Process Identification)**：PID, Parent PID, User ID。
2. **处理器状态信息 (Processor State Information)**：
   - **寄存器内容 (Registers)**：当进程被暂停时，必须把PC（程序计数器）、PSW（状态字）等寄存器的值存在PCB里，以便下次恢复现场。
3. **进程控制信息 (Process Control Information)**：
   - 调度状态（是Ready还是Blocked？）、优先级、打开的文件列表等。

## 第四部分：进程控制 (Process Control) 🔥 易混淆点

*对应课件 Page 51-59*

### 1. 执行模式 (Modes of Execution)

- **User Mode (用户态)**：权限低，只能跑普通指令。
- **Kernel/System/Control Mode (内核态)**：权限高，能跑**特权指令 (Privileged Instructions)**，能动内存、动I/O。
- **PSR (Program Status Register)**：里面有一位 (Bit) 专门标记当前是用户态还是内核态。

### 2. 进程切换 (Process Switching) vs 模式切换 (Mode Switching)

**这是这一章最大的坑，一定要分清！**

| **特性**     | **模式切换 (Mode Switch)**                             | **进程切换 (Process Switch)**                                |
| ------------ | ------------------------------------------------------ | ------------------------------------------------------------ |
| **定义**     | 用户态 <-> 内核态                                      | 进程A -> 进程B                                               |
| **发生场景** | 遇到中断、系统调用时                                   | 调度器决定换人时                                             |
| **消耗**     | **小** (只存少量寄存器，不需要动内存映射)              | **大** (要存整个PCB，要更新内存表，刷新Cache/TLB)            |
| **关系**     | 进程切换**必须**在内核态下进行（所以必然伴随模式切换） | 模式切换**不一定**导致进程切换（比如只是处理个简单的中断，处理完又回到原进程） |

### 3. 何时切换进程？

- **Interrupt (中断)**：时钟中断（时间片到了）、I/O中断。
- **Trap (陷阱)**：程序出错（除以零）。
- **Supervisor Call (系统调用)**：程序请求OS服务（打开文件）。

### 4. 进程切换的步骤 (Steps for Process Switch)

1. 保存 CPU 上下文（PC, Registers）到当前进程的 PCB。
2. 更新当前进程状态（如 Running -> Ready）。
3. 把当前进程移到相应的队列。
4. **调度决策 (Selection)**：选下一个谁跑？
5. 更新被选中进程的 PCB（变为 Running）。
6. 更新内存管理结构（TLB等）。
7. **恢复上下文 (Restore Context)**：把被选中进程 PCB 里的寄存器值填回 CPU。

## 第五部分：OS 的执行模型

*对应课件 Page 60-61*

OS 代码自己怎么跑？

1. **无进程内核 (Nonprocess Kernel)**：OS 不是进程，是所有进程的“保姆”。
2. **在用户进程中执行 (Execution within User Processes)**：最常见（Unix/Linux/Windows）。OS 代码就像是用户程序调用的一个子程序，在用户进程的上下文中（内核态）运行。
3. **基于进程的 OS (Process-Based OS)**：OS 的功能通过独立的系统进程来实现。

## 📝 必背英文术语表 (Exam Vocabulary)

| **英文**                        | **中文**    | **备注**                   |
| ------------------------------- | ----------- | -------------------------- |
| **Process Control Block (PCB)** | 进程控制块  | 进程存在的唯一标志         |
| **Dispatcher**                  | 分派器      | 负责切换进程的小程序       |
| **Trace**                       | 轨迹        | 指令执行序列               |
| **Round-Robin**                 | 轮转        | 一种调度策略（时间片轮转） |
| **Swapping**                    | 交换        | 内存 <-> 磁盘              |
| **Suspended**                   | 挂起        | 在磁盘上等待               |
| **Preemption**                  | 抢占        | 强行剥夺 CPU（如超时）     |
| **Context Switch**              | 上下文切换  | 即进程切换，开销大         |
| **Mode Switch**                 | 模式切换    | 用户态 <-> 内核态          |
| **User/Kernel Mode**            | 用户/内核态 | 权限级别的区分             |
| **Privileged Instruction**      | 特权指令    | 只能在内核态执行           |

## 💡 常见简答题思路

1. **进程和程序的本质区别？**
   - 动与静；PCB的存在。
2. **画出五状态转换图，并标注转换原因。**
   - 重点标记：Running -> Ready (Time-out), Running -> Blocked (Wait for event).
3. **为什么 Mode Switch 比 Process Switch 快？**
   - Mode Switch 只需要保存/恢复少量与指令执行相关的寄存器，不用切换内存空间（Memory Space），不用刷 TLB/Cache。Process Switch 涉及整个环境的改变。