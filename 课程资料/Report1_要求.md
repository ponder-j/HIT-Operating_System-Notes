# 1. x86系统架构概览[](https://os.guojunhit.cn/Intelx86/chap02.html#x86 "永久链接至标题")

## 1.1. 系统级体系结构概览[](https://os.guojunhit.cn/Intelx86/chap02.html#id1 "永久链接至标题")

参照图 `2.1` ，需要了解图中的所有系统级寄存器和数据结构，在后面的章节中都有介绍。

以下内容是要重点掌握的：

- Global and Local Descriptor Tables
    
- System Segments, Segment Descriptors, and Gates
    
- Task-State Segments and Task Gates
    
- Interrupt and Exception Handling
    
- Memory Management
    
- System Registers
    

## 1.2. 实模式和保护模式转换[](https://os.guojunhit.cn/Intelx86/chap02.html#id2 "永久链接至标题")

了解两种操作模式进行转换，所需要进行哪些修改。

## 1.3. 80x86系统指令寄存器[](https://os.guojunhit.cn/Intelx86/chap02.html#id3 "永久链接至标题")

了解和掌握相关寄存器：

- 标志寄存器 `EFLAGS`
    
- 内存管理寄存器，包括 `GDTR` ，`LDTR` ，`IDTR` ，`TR`
    
- 控制寄存器，包括 `CR0` 至 `CR3`
    

## 1.4. 系统指令[](https://os.guojunhit.cn/Intelx86/chap02.html#id4 "永久链接至标题")

了解和掌握相关系统指令：

- `LGDT`
    
- `SGDT`
    
- `LIDT`
    
- `SIDT`
    
- `LLDT`
    
- `SLDT`
    
- `LTR`
    
- `STR`