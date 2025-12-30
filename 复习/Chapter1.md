# 💻 操作系统第1章：计算机系统概述 (Computer System Overview) 复习指南

## 🌟 核心逻辑

这一章看似在大谈硬件，其实是在为操作系统（OS）铺路。OS的作用是管理硬件，所以你必须先了解：

1. **CPU是怎么工作的？** (指令执行、中断)
2. **内存不够快怎么办？** (存储器层次结构、Cache)
3. **设备太慢怎么办？** (I/O技术、中断、DMA)

## 第一部分：基本组成 (Basic Elements)

*对应课件 Page 4-15*

计算机由四大金刚组成，它们通过**系统总线 (System Bus)** 连接：

1. **处理器 (Processor / CPU)**
   - **功能**：控制操作、处理数据。
   - **核心寄存器 (Registers)** —— **必考！要分清谁是干嘛的**：
     - **PC (Program Counter)**：保存**下一条**要取指令的地址。（注意是下一条，不是当前条）。
     - **IR (Instruction Register)**：保存**当前正在执行**的指令。
     - **MAR (Memory Address Register)**：想访问内存哪个地址？放这里。
     - **MBR (Memory Buffer Register)**：从内存读出来的数据/要写入内存的数据，暂存在这。
     - **I/O AR & I/O BR**：和I/O模块交换地址和数据的寄存器。
2. **主存 (Main Memory)**
   - **特性**：易失性 (Volatile) —— 断电数据就没了。也叫 Real Memory / Primary Memory。
3. **I/O 模块 (I/O Modules)**
   - **功能**：连接外部设备（硬盘、网卡等）和CPU/内存的桥梁。
4. **系统总线 (System Bus)**
   - **功能**：在CPU、内存、I/O之间传输数据、地址和控制信号。

## 第二部分：指令执行 (Instruction Execution)

*对应课件 Page 16-19*

最基础的**指令周期 (Instruction Cycle)** 只有两步：

1. **取指 (Fetch)**：CPU从内存读指令（PC -> MAR -> MBR -> IR）。
2. **执行 (Execute)**：CPU解释并执行指令（可能涉及计算、读写内存、I/O）。

- **程序执行示例**：PPT第19页的加法例子要看懂（PC怎么变，AC累加器怎么变）。

## 第三部分：中断 (Interrupts) 🔥🔥 超级重点

*对应课件 Page 20-34*

为什么要有中断？

为了提高处理器的利用率 (Processor Utilization)。

- **原因**：I/O设备（如打印机、硬盘）比CPU慢几十万倍。如果让CPU干等着I/O完成（忙等待），太浪费了。有了中断，CPU可以让I/O自己干活，自己去跑别的程序，等I/O干完了发个信号（中断）告诉CPU。

### 1. 中断的类型 (Classes of Interrupts)

- **Program**：程序出错了（除以零、非法指令）。
- **Timer**：定时器时间到了（用于多任务调度）。
- **I/O**：I/O操作完成或出错了。
- **Hardware failure**：掉电、内存校验错误。

### 2. 带中断的指令周期

- 在“取指”和“执行”之后，加了一个**中断阶段 (Interrupt Stage)**。
- CPU每次执行完一条指令，都会检查：**“有人敲门（有中断）吗？”**
  - 没有 -> 继续取下一条指令。
  - 有 -> 暂停当前程序 -> 保存现场 -> 跳去执行中断处理程序 (Interrupt Handler)。

### 3. 中断处理过程 (Simple Interrupt Processing)

关键动作：**保存现场 (Save Context)**。

- 必须保存 **PC (程序计数器)** 和 **PSW (程序状态字)** 等寄存器信息到栈 (Stack) 中，这样处理完中断回来，还能接着之前的进度继续跑。

### 4. 多重中断 (Multiple Interrupts)

如果处理中断时，又来了一个中断怎么办？

- **方案A：顺序处理 (Sequential)** —— 正在处理时，禁止新的中断（Disable Interrupts）。大家排队。
- **方案B：嵌套处理 (Nested)** —— **优先级 (Priority)** 高的可以插队。

## 第四部分：存储器层次结构 (Memory Hierarchy) 🔥 核心考点

*对应课件 Page 35-40*

**金字塔结构**：从顶到底（寄存器 -> Cache -> 内存 -> 磁盘 -> 磁带）。

- **规律**（向下走）：
  - **成本 (Cost)**：越来越便宜。
  - **容量 (Capacity)**：越来越大。
  - **速度 (Access Time)**：越来越慢。
  - **CPU访问频率**：越来越低。

**局部性原理 (Principle of Locality)**：

- 这是存储分层能生效的根本原因。
- **含义**：CPU在一段时间内访问的数据倾向于**聚集**在某些区域（不管是指令还是数据）。所以我们把这部分“热点数据”放在快的Cache里，就能骗过CPU，让它觉得内存很快。

## 第五部分：高速缓存 (Cache Memory)

*对应课件 Page 41-44*

- **对OS不可见**：Cache主要是硬件管理的，OS通常不需要插手。
- **目的**：利用局部性原理，结合小而快的存储（Cache）和大而慢的存储（Main Memory），提供接近Cache的速度和接近内存的容量。
- **结构**：
  - **Block (Slot/Line)**：Cache和内存交换数据的单位（块）。
  - **Tag**：用来标记这个块到底是内存里的哪一块。
- **命中率 (Hit Ratio)**：在Cache里找到数据的概率。越高越好。

## 第六部分：I/O 技术 (I/O Techniques) 🔥 常考对比

*对应课件 Page 45-48*

这是三种I/O进化的方式，**一定要背得下来区别**：

1. **程序控制 I/O (Programmed I/O)**
   - **做法**：CPU不断地询问设备“好了吗？好了吗？” (Busy Waiting)。
   - **缺点**：CPU被绑死在查询上，效率极低。
2. **中断驱动 I/O (Interrupt-driven I/O)**
   - **做法**：CPU发令后去干别的，设备好了发中断通知CPU。
   - **缺点**：虽然CPU不用等了，但**每次传一个字 (Word)** 都要打断CPU一次。如果要传大量数据（比如读大文件），CPU会被中断烦死，效率还是不够高。
3. **直接内存访问 (DMA - Direct Memory Access)**
   - **做法**：CPU把重活交给**DMA模块**。
   - **流程**：CPU告诉DMA“读磁盘X地址的数据，存到内存Y地址，长度Z”，然后CPU甩手不管。DMA直接在磁盘和内存间搬运数据。搬完了才发**一次**中断告诉CPU。
   - **优点**：CPU只在开始和结束参与，适合**大数据块传输**。

## 第七部分：多处理器与多核 (Multiprocessor/Multicore)

*对应课件 Page 49-54*

1. **对称多处理器 (SMP - Symmetric Multiprocessors)**
   - **特征**：
     - 多个类似的处理器。
     - **共享**同一个主存和I/O。
     - 地位平等 (Symmetric)，都能干同样的事。
     - 由一个集成的OS控制。
   - **优点**：性能强、可用性高（坏了一个CPU还能跑）、易扩展。
2. **多核 (Multicore)**
   - **定义**：在一块硅片 (Chip) 上集成两个或多个处理器核心 (Cores)。
   - **结构**：每个核有自己的L1 Cache，通常共享L2或L3 Cache。
   - **例子**：Intel Core i7。

## 📝 必背英文术语表 (Exam Vocabulary)

| **英文**                            | **中文**       | **备注**                        |
| ----------------------------------- | -------------- | ------------------------------- |
| **Processor (CPU)**                 | 处理器         | 核心部件                        |
| **Main Memory (Volatile)**          | 主存（易失性） | 掉电丢数据                      |
| **System Bus**                      | 系统总线       | 传输通道                        |
| **Instruction Cycle**               | 指令周期       | Fetch -> Execute -> Interrupt   |
| **Interrupts**                      | 中断           | 提高CPU利用率的关键             |
| **Memory Hierarchy**                | 存储器层次结构 | 寄存器-Cache-内存-外存          |
| **Principle of Locality**           | 局部性原理     | Cache生效的理论基础             |
| **Programmed I/O**                  | 程序控制I/O    | 忙等待，效率低                  |
| **Interrupt-driven I/O**            | 中断驱动I/O    | 解放等待，但数据传输仍需CPU干预 |
| **DMA (Direct Memory Access)**      | 直接内存访问   | CPU仅仅介入开始和结束，效率最高 |
| **SMP (Symmetric Multiprocessors)** | 对称多处理器   | 共享内存，地位平等              |