# 🐧 操作系统第2章：操作系统概述 (Operating System Overview) 复习指南

## 🌟 核心逻辑：OS 是怎么来的？

操作系统的进化史，其实就是一部**“压榨”硬件性能**的历史。

- 硬件太贵太快，人太慢 -> **批处理** (Batch)
- CPU太快，I/O太慢，CPU老在等 -> **多道程序** (Multiprogramming)
- 人想和电脑实时交互 -> **分时系统** (Time-Sharing)

## 第一部分：操作系统的目标与功能 (Objectives and Functions)

*对应课件 Page 4-10*

### 1. 操作系统是什么？

- **作为接口 (User/Computer Interface)**：让硬件变得好用（Convenience）。它向下控制硬件，向上给用户/程序提供服务（API, ABI, ISA）。
- **作为资源管理者 (Resource Manager)**：让硬件用得高效（Efficiency）。管理CPU、内存、I/O设备等。
- **可演进性 (Ability to Evolve)**：能升级换代，适应新硬件。

## 第二部分：操作系统的演化 (Evolution of Operating Systems) 🔥🔥 必考重点

*对应课件 Page 11-28*

这是本章最核心的故事线，一定要分清每个阶段解决了什么问题。

### 1. 串行处理 (Serial Processing)

- **状态**：**没有操作系统**。程序员直接拨开关、看灯泡来操作硬件。
- **缺点**：
  - **调度 (Scheduling)**：得预约上机，时间安排很难完美。
  - **准备时间 (Setup time)**：装磁带、加载编译器都要人工，CPU大部分时间在空转。

### 2. 简单批处理系统 (Simple Batch Systems)

- **核心发明**：**监控程序 (Monitor)**。
  - 这是现代OS的祖先。它常驻内存，负责把一个接一个的作业 (Job) 自动加载并运行。
- **用户不再直接操作机器**：用户把卡片给操作员，操作员把卡片喂给机器。
- **JCL (Job Control Language)**：作业控制语言（比如 `$JOB`, `$LOAD`），告诉Monitor该干嘛。
- **硬件支持**：为了保护Monitor不被用户程序搞坏，引入了**双模式 (Modes of Operation)**：
  - **用户模式 (User Mode)**：跑用户程序。
  - **内核模式 (Kernel Mode)**：跑Monitor，能执行特权指令（Privileged Instructions）。

### 3. 多道批处理系统 (Multiprogrammed Batch Systems)

- **解决痛点**：I/O设备（磁带/磁盘）太慢了！单道程序时，一做I/O，CPU就傻等。
- **核心思想**：**内存里同时装多个程序**。
  - 当程序A在等I/O时，CPU立刻切换去跑程序B。
  - **目的**：最大化CPU利用率 (Maximize Processor Utilization)。
- **课件例子 (Page 21-24)**：
  - Uniprogramming: CPU利用率极低（如3.2%）。
  - Multiprogramming: 多个任务交替，CPU利用率翻倍。

### 4. 分时系统 (Time-Sharing Systems)

- **解决痛点**：批处理虽然CPU爽了，但**人很不爽**。用户没法交互（改个Bug要等几小时出结果）。
- **核心思想**：**时间片 (Time Slicing)**。
  - 把CPU时间切成很短的片（如0.2秒），轮流分给每个用户。
  - 因为切得够快，每个用户都觉得自己在独占计算机。
- **目的**：最小化**响应时间 (Minimize Response Time)**。
- **例子**：CTSS (Compatible Time-Sharing System)。

## 第三部分：主要成就 (Major Achievements)

*对应课件 Page 29-41*

操作系统在进化过程中发展出了几个核心概念：

### 1. 进程 (Process)

- **定义**：**正在执行中的程序 (A program in execution)**。
- **由来**：为了管理多道程序并发时的混乱（死锁、同步问题）。
- **组成**：
  - 可执行程序 (Code)
  - 数据 (Data)
  - **执行上下文 (Execution Context / Process State)**：包括寄存器值、PC值等，一定要保存这个才能暂停/恢复进程。

### 2. 内存管理 (Memory Management)

- **核心需求**：
  - **进程隔离 (Process Isolation)**：A程序不能改B程序的数据。
  - **自动分配 (Automatic Allocation)**。
- **虚拟内存 (Virtual Memory)**：
  - **逻辑地址 vs 物理地址**：程序以为自己有很大连续内存，其实是分散在物理内存甚至磁盘上的。
  - **分页 (Paging)**：把程序切成固定大小的块（Page），物理内存切成框（Frame），建立映射。

## 第四部分：现代操作系统特征 (Modern Operating Systems)

*对应课件 Page 44-48*

现代OS（如Windows, Linux）通常具备以下架构特征：

1. **微内核 (Microkernel)**：内核只留最核心功能（调度、IPC），其他扔到用户态。稳定性高。
2. **多线程 (Multithreading)**：一个进程里可以有多个执行流（Thread），并发度更高。
3. **对称多处理 (SMP)**：多核CPU共享内存，地位平等。
4. **虚拟化 (Virtualization)**：
   - **虚拟机 (Virtual Machine)**：在物理机上模拟出多台逻辑计算机。
   - **VMM (Virtual Machine Monitor / Hypervisor)**：介于硬件和操作系统之间，负责管理虚拟机。

## 第五部分：Linux/Windows/Unix 架构

*对应课件 Page 52-63*

- **Linux**：
  - **宏内核 (Monolithic Kernel)**：所有功能都在内核里（效率高）。
  - **模块化 (Modular)**：虽然是宏内核，但支持动态加载模块（Loadable Modules），灵活。
- **Windows**：
  - 底层有硬件抽象层 (HAL)，内核态包含图形驱动（这导致显卡驱动崩了容易蓝屏）。

## 📝 必背英文术语表 (Exam Vocabulary)

| **英文**                | **中文**      | **核心考点**                      |
| ----------------------- | ------------- | --------------------------------- |
| **Serial Processing**   | 串行处理      | 无OS，人工操作                    |
| **Simple Batch System** | 简单批处理    | 引入 Monitor (监控程序)           |
| **Multiprogramming**    | 多道程序设计  | **目的：提高CPU利用率** (Batch用) |
| **Time-Sharing**        | 分时系统      | **目的：减少响应时间** (交互用)   |
| **Time Slicing**        | 时间片轮转    | 分时系统的核心技术                |
| **User/Kernel Mode**    | 用户/内核模式 | 硬件保护机制，防止用户搞坏Monitor |
| **Process**             | 进程          | A program in execution            |
| **Virtual Memory**      | 虚拟内存      | 逻辑地址 != 物理地址              |
| **Microkernel**         | 微内核        | 内核精简，稳定性好                |
| **Monolithic Kernel**   | 宏内核        | Linux/Unix典型结构，效率高        |
| **Virtualization**      | 虚拟化        | VMM, Hypervisor                   |

## 💡 常见简答题思路

1. **多道程序 (Multiprogramming) 和 分时 (Time-Sharing) 的区别？**
   - **多道程序**是为了让CPU别闲着（利用率），主要用于批处理。
   - **分时**是为了让人别闲着（响应时间），主要用于交互系统。
2. **什么是进程？和程序有什么区别？**
   - 程序是静止的代码（死），进程是运行中的实例（活），包含了状态（寄存器、栈）。