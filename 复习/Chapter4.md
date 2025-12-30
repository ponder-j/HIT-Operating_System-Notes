# 🧵 操作系统第4章：线程 (Threads) 复习指南

## 🌟 核心逻辑：从“重”到“轻”

这一章的核心思想就是把进程的两个职能拆开：

1. **资源所有者 (Resource Ownership)**：依然归**进程 (Process)** 管。
2. **调度/执行单位 (Scheduling/Execution)**：交给**线程 (Thread)** 管。

所以，线程又被称为 **Lightweight Process (LWT, 轻量级进程)**。

## 第一部分：进程 vs 线程 (Processes and Threads)

*对应课件 Page 5-11*

### 1. 拆分后的定义

- **进程 (Process)**：资源分配的单位 (Unit of Resource Ownership)。拥有虚拟地址空间、内存、文件句柄等。
- **线程 (Thread)**：调度和分派的单位 (Unit of Dispatching)。它是被OS送到CPU上去跑的那个实体。

### 2. 多线程 (Multithreading)

- **定义**：一个进程里同时有多个执行路径 (Multiple concurrent paths of execution within a single process)。
- **共享什么 (Shared)**：所有线程共享同一个**进程地址空间 (Address Space)** 和 **资源 (Resources)**（如打开的文件）。
- **独占什么 (Per-thread)**：每个线程必须有自己独立的“私房钱”才能跑：
  - **执行状态 (Execution State)**：Running, Ready 等。
  - **上下文 (Context)**：程序计数器 (PC) 和 寄存器 (Registers)。
  - **栈 (Execution Stack)**：保存函数调用记录和局部变量。

## 第二部分：为什么要用线程？(Key Benefits)

*对应课件 Page 12-13*

相比于搞多个进程，搞多个线程有四大优势（背诵点）：

1. **创建快 (Creation)**：新建线程比新建进程快得多（因为不用分配新内存空间）。
2. **终止快 (Termination)**：销毁线程快。
3. **切换快 (Switching)**：线程切换比进程切换快（因为不用切换页表/地址空间）。
4. **通信快 (Communication)**：线程间直接读写共享内存就能通信，不需要像进程间通信 (IPC) 那样求助于内核。

## 第三部分：线程的状态与同步 (States & Synchronization)

*对应课件 Page 14-18*

### 1. 线程状态

- 线程也有 **Running, Ready, Blocked** 三种基本状态。
- **关键点**：
  - **挂起 (Suspending)** 是**进程级**的概念。如果一个进程被挂起（Swap out 到硬盘），它里面的**所有线程**也都算被挂起了（因为内存都没了，线程皮之不存毛将焉附）。
  - **终止 (Termination)**：如果进程被杀掉，里面所有线程全部陪葬。

### 2. 同步 (Synchronization)

- 因为所有线程共享同一块内存，如果它们同时改一个变量（比如链表），就会出乱子。所以必须要有**同步机制**（后面章节会细讲）。

## 第四部分：用户级线程 vs 内核级线程 (ULT vs KLT) 🔥🔥🔥 必考对比

*对应课件 Page 19-26*

这是本章最硬核的考点，一定要把两者的优缺点分得清清楚楚。

### 1. 用户级线程 (ULT - User-Level Threads)

- **原理**：OS 内核根本**不知道**线程的存在。线程的管理（创建、调度）全靠用户空间的一个 **Threads Library (线程库)** 来做。
- **优点**：
  - **切换极快**：不需要内核态特权，不需要 **Mode Switch (模式切换)**。
  - **调度灵活**：应用程序可以自己决定调度策略（比如专门为某个算法定制）。
  - **跨平台**：可以在任何OS上跑（只要有线程库）。
- **缺点**：
  - **阻塞问题**：如果一个线程发起系统调用（System Call）被阻塞了，**整个进程**里的所有线程都会被阻塞（因为内核看来这就是一个进程在等）。
  - **无法利用多核**：内核只把它当成一个进程，所以一次只能分给它一个CPU核心。哪怕你有100个线程，也只能在一个核上轮流跑。
- **补救措施**：**Jacketing** (包一层)。把阻塞的系统调用包成一个非阻塞的调用，防止全家被锁死。

### 2. 内核级线程 (KLT - Kernel-Level Threads)

- **原理**：OS 内核亲自管理线程。Windows, Linux, Solaris 都是这种。
- **优点**：
  - **真正的并发**：可以在多个CPU核心上同时跑同一个进程的多个线程。
  - **不连坐**：一个线程阻塞了，内核可以调度同一个进程里的其他线程继续跑。
- **缺点**：
  - **慢**：线程切换需要进出内核 (**Mode Switch**)，开销比 ULT 大。

## 第五部分：混合模型 (Combined Approaches)

*对应课件 Page 27-28*

为了结合 ULT 的快和 KLT 的并发，搞出了混合模型（如 Solaris）。

- **多对多 (M:N)**：M 个用户线程映射到 N 个内核线程上。
- **模型总结表**：
  - **1:1** (Unix, Linux)：一个线程对应一个内核实体。
  - **M:1** (早期的线程库)：多个线程挤在一个进程壳子里（就是纯 ULT）。
  - **M:N** (Solaris, TRIX)：灵活映射。

## 📝 必背英文术语表 (Exam Vocabulary)

| **英文**                        | **中文**     | **备注**                           |
| ------------------------------- | ------------ | ---------------------------------- |
| **Multithreading**              | 多线程       | 单进程内多执行流                   |
| **Lightweight Process (LWT)**   | 轻量级进程   | 线程的别名                         |
| **Resource Ownership**          | 资源所有权   | 归进程管                           |
| **Dispatching/Scheduling**      | 调度         | 归线程管                           |
| **User-Level Thread (ULT)**     | 用户级线程   | 库管理，快，由于阻塞导致全进程阻塞 |
| **Kernel-Level Thread (KLT)**   | 内核级线程   | 内核管理，慢，支持多核并行         |
| **Jacketing**                   | 包装技术     | 解决ULT阻塞问题的技巧              |
| **Mode Switch**                 | 模式切换     | KLT切换时必须发生，ULT不需要       |
| **RPC (Remote Procedure Call)** | 远程过程调用 | 课件中用作多线程性能收益的例子     |

## 💡 常见简答题思路

1. **ULT 和 KLT 的主要区别是什么？（从调度、性能、阻塞影响三个方面回答）**
   - **调度**：ULT由库调度，KLT由OS调度。
   - **性能**：ULT切换不需要进内核，快；KLT慢。
   - **阻塞**：ULT一人阻塞全家阻塞；KLT一人阻塞别人照跑。
2. **为什么有了进程还要引入线程？**
   - 为了在同一个应用内部实现并发（Concurrency），同时减少创建和切换的开销（Overhead）。