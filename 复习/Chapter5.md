# 🔒 操作系统第5章：互斥和同步 (Mutual Exclusion & Synchronization)

## 🌟 核心逻辑：为什么会“打架”？

在多道程序设计（Multiprogramming）中，多个进程可能同时去抢同一个资源（比如打印机、共享变量）。

- 如果不加控制，大家乱抢，就会导致数据出错 —— 这叫 **Race Condition (竞争条件)**。
- 为了解决这个问题，我们需要立规矩，让关键时刻只能有一个人操作 —— 这叫 **Mutual Exclusion (互斥)**。

## 第一部分：并发的基本原理 (Principles of Concurrency)

*对应课件 Page 3-18*

### 1. 关键术语 (Key Terms) —— 必考定义

- **Race Condition (竞争条件)**：多个进程读写共享数据，最终结果取决于谁跑得快（执行顺序不确定）。
- **Critical Section (临界区)**：**代码中**访问共享资源的那一段代码。
  - *复习口诀*：一次只能有一个进程在临界区里。
- **Mutual Exclusion (互斥)**：当一个进程在临界区时，其他进程不能进。
- **Starvation (饥饿)**：一个进程长期得不到资源，虽然没死锁，但也跑不了。
- **Deadlock (死锁)**：两个进程互相等着对方手里的资源，谁也不放手，卡死了（下一章细讲）。

### 2. 互斥的三大要求 (Requirements for Mutual Exclusion)

要想设计一个好的互斥方案，必须满足：

1. **强制互斥**：临界区里同时只能有一个人。
2. **不干涉**：没进临界区的进程不能拦着别人进。
3. **不饥饿/无死锁**：想进的进程最终得能进得去。

## 第二部分：实现互斥的方法 (Approaches)

*对应课件 Page 19-38*

怎么实现互斥？人类想出了三类办法：

### 方法一：软件方法 (Software Approaches)

- **Dekker算法 / Peterson算法**。
- **原理**：单纯靠代码逻辑（Flag变量、Turn变量）来谦让。
- **缺点**：逻辑巨复杂，容易写错；且需要 **Busy Waiting (忙等待)** —— 进不去的进程会在 `while` 循环里空转，浪费CPU。

### 方法二：硬件支持 (Hardware Support)

1. **关中断 (Interrupt Disabling)**：
   - **原理**：CPU不理中断，就不会切换进程，我就可以独占CPU把临界区跑完。
   - **缺点**：**只对单处理器有效**（多核CPU关了一个核，别的核还能跑）；把控制权交给用户太危险（用户关了中断不复原怎么办？）。
2. **专用机器指令 (Special Machine Instructions)**：
   - **Test and Set (TAS)** / **Compare and Swap (CAS)**。
   - **原理**：硬件保证“读-写”这两个动作是**原子性 (Atomic)** 的，不可打断。
   - **优点**：适用于多处理器。
   - **缺点**：依然是 **Busy Waiting**。

### 方法三：操作系统/语言支持 (OS/Language Support) —— **核心重点**

因为忙等待太浪费，OS 提供了更高级的工具：

1. **Semaphore (信号量)**
2. **Monitor (管程)**
3. **Message Passing (消息传递)**

## 第三部分：信号量 (Semaphores) 🔥🔥🔥 全书最核心考点

*对应课件 Page 39-55*

一定要理解信号量怎么工作，它是解决同步问题的万能钥匙。

### 1. 定义

- 本质是一个**整数变量 (Integer value)**。
- 只能通过两个**原子操作**来访问：
  - **wait(s) / P(s)**：**“申请”**。如果 s > 0，s 减 1，继续执行；如果 s <= 0，进程**阻塞 (Block)**（睡觉去，别忙等待）。
  - **signal(s) / V(s)**：**“释放”**。s 加 1；如果有进程在等，叫醒它 (Wake up)。

### 2. 分类

- **Binary Semaphore (二元信号量/互斥锁)**：值只能是 0 或 1。用于**互斥**（锁）。
- **Counting Semaphore (计数信号量)**：值可以是任意整数。用于**资源计数**（比如缓冲区有 N 个空位）。

### 3. 经典问题：生产者/消费者 (Producer/Consumer Problem)

- **场景**：生产者往 Buffer 放数据，消费者取数据。Buffer 满了不能放，空了不能取。
- **信号量设置**：
  - `mutex = 1`：保护 Buffer 的互斥访问。
  - `empty = N`：空位数量（一开始是 N）。
  - `full = 0`：满位数量（一开始是 0）。
- **代码逻辑**（一定要看懂 PPT 里的伪代码）：
  - Producer: `wait(empty)` -> `wait(mutex)` -> 放数据 -> `signal(mutex)` -> `signal(full)`
  - Consumer: `wait(full)` -> `wait(mutex)` -> 取数据 -> `signal(mutex)` -> `signal(empty)`

## 第四部分：管程 (Monitors)

*对应课件 Page 56-65*

- **为什么要有管程？** 信号量虽然好用，但容易写错（`wait` 和 `signal` 写反了就死锁了）。
- **定义**：一种程序设计语言结构（像 Java 的 `synchronized`）。
  - 它把共享变量和操作这些变量的函数**封装**在一起。
  - **自动互斥**：编译器保证任何时候只能有一个线程在管程里跑。
- **条件变量 (Condition Variables)**：
  - `cwait(c)`：条件不满足，挂起。
  - `csignal(c)`：条件满足了，唤醒别人。

## 第五部分：消息传递 (Message Passing)

*对应课件 Page 66-73*

- **特点**：不仅能同步，还能交换数据。特别适合**分布式系统**（不同机器之间）。
- **原语**：`send(destination, message)` 和 `receive(source, message)`。
- **阻塞/非阻塞**：
  - **Blocking send/receive**：发完/收完之前一直等（如打电话）。
  - **Non-blocking**：发完就走，不管收到没（如发短信）。

## 第六部分：读者-写者问题 (Readers/Writers Problem)

*对应课件 Page 74-77*

- **场景**：一个文件。
  - **读 (Read)**：可以多人同时读。
  - **写 (Write)**：必须独占。有人写的时候，不能有别人读或写。
- **两种优先策略**：
  1. **读者优先 (Readers Priority)**：只要有一个读者在读，随后的读者都能进来读。写者可能**饥饿**。
  2. **写者优先 (Writers Priority)**：只要写者申请写，后续的读者就别想进来了，等写完再说。

## 📝 必背英文术语表 (Exam Vocabulary)

| **英文**                        | **中文** | **核心含义**               |
| ------------------------------- | -------- | -------------------------- |
| **Concurrency**                 | 并发     | 逻辑上的同时发生           |
| **Race Condition**              | 竞争条件 | 结果依赖于执行顺序         |
| **Critical Section**            | 临界区   | 访问共享资源的代码段       |
| **Mutual Exclusion (Mutex)**    | 互斥     | 临界区只能进一人           |
| **Atomic Operation**            | 原子操作 | 不可分割，要么做完要么不做 |
| **Busy Waiting / Spin Waiting** | 忙等待   | 循环查询，浪费CPU          |
| **Semaphore**                   | 信号量   | 解决同步的工具 (P/V操作)   |
| **Monitor**                     | 管程     | 高级同步机制，自动互斥     |
| **Deadlock**                    | 死锁     | 互相等待，永久阻塞         |
| **Starvation**                  | 饥饿     | 长期得不到调度             |

## 💡 常见简答题思路

1. **Busy Waiting 和 Blocking 的区别？**
   - **Busy Waiting**：进程在CPU上空转（`while` loop），浪费CPU周期。适用于硬件指令或多核短时间等待。
   - **Blocking**：进程放弃CPU，进入等待队列，直到被唤醒。适用于I/O等待或信号量，节省CPU。
2. **信号量中 wait/signal 操作必须是原子性的吗？为什么？**
   - 必须是。如果 `wait` 操作减1的过程被打断，两个进程可能同时读到 s>0，同时进入临界区，互斥就失效了。
3. **什么是“竞争条件”？举个生活中的例子。**
   - 例子：两个人同时往同一个银行账户存钱。如果读取余额和写入余额没有互斥，最后余额可能只增加了一笔。