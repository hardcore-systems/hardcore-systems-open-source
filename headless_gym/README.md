# Headless Systems Gym (Implicit State)

A collection of lightweight, high-performance systems engineering simulators exposing standard Gym-like APIs. Designed for reinforcement learning and coding agents to test and evaluate their systems diagnosis capabilities.

## 🚀 Gyms Included

1. `ConsistentHashGym`: Consistent Hashing virtual-node load balancer.
2. `EBPFRedirectGym`: Linux eBPF SOCKMAP / TProxy traffic redirection simulator.
3. `LsmCompactionGym`: LSM Storage Engine compaction and write amplification analyzer.
4. `RaftConsensusGym`: Distributed Consensus / Leader Election and Network Partition simulator.
5. `BorrowCheckerGym`: Rust borrow checker static analysis compiler error simulator.
6. `DailyDiagnosticsGym`: MySQL transaction gap locking and CPU scheduler diagnostics.


## 📊 Gym Architecture & Reference Metrics

The environments in `headless_gym` return standard OpenAI-Gym-style observations as structured JSON. They are designed for reward optimization in RL:
* **ConsistentHashGym**: Computes load balance standard deviation across node rings. Useful for testing hashing virtual-node distributions (target: standard deviation approach **0.0** as virtual nodes approach **infinity**).
* **EBPFRedirectGym**: Simulates networking metrics where:
  - `SOCKMAP` option yields `latency_us` = `2.0 + size_kb * 0.1` and `cpu_softirq` = `0.5%`.
  - `TProxy` option yields `latency_us` = `12.0 + size_kb * 0.5` and `cpu_softirq` = `4.5%`.
* **LsmCompactionGym**: Tracks SSTable volume write amplification factors across level thresholds.
* **BorrowCheckerGym**: Simulates compile-time borrow lifetimes, returning formal `CompilationError` payloads on lifetime overlaps (Rust compiler borrow check emulation).

## 📄 Academic References
- Lehman & Yao, *"Efficient Locking for Concurrent Operations on B-Trees"* (1981).
- Ongaro & Ousterhout, *"In Search of an Understandable Consensus Algorithm"* (2014).
- O'Neil et al., *"The Log-Structured Merge-Tree (LSM-Tree)"* (1996).
