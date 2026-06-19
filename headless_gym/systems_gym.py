import math
import hashlib

class ConsistentHashGym:
    """Consistent Hashing Simulation Gym"""
    def __init__(self, num_nodes=3, vnodes=10):
        self.vnodes = vnodes
        self.ring = {}  # hash -> node_name
        self.nodes = set()
        for i in range(num_nodes):
            self.add_node(f"node_{i}")

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16) % 360

    def add_node(self, node):
        self.nodes.add(node)
        for i in range(self.vnodes):
            vnode_key = f"{node}-vnode-{i}"
            h = self._hash(vnode_key)
            self.ring[h] = node

    def remove_node(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            for i in range(self.vnodes):
                vnode_key = f"{node}-vnode-{i}"
                h = self._hash(vnode_key)
                if h in self.ring:
                    del self.ring[h]

    def get_node_for_key(self, key):
        if not self.ring:
            return None
        h = self._hash(key)
        for ring_h in sorted(self.ring.keys()):
            if h <= ring_h:
                return self.ring[ring_h]
        return self.ring[min(self.ring.keys())]

    def get_stats(self, num_keys=1000):
        if not self.nodes:
            return {"std_dev": 0.0, "distribution": {}}
        counts = {node: 0 for node in self.nodes}
        for k in range(num_keys):
            node = self.get_node_for_key(f"key-{k}")
            if node:
                counts[node] += 1
        mean = num_keys / len(self.nodes)
        variance = sum((c - mean) ** 2 for c in counts.values()) / len(self.nodes)
        std_dev = math.sqrt(variance)
        return {"std_dev": round(std_dev, 2), "distribution": counts}


class EBPFRedirectGym:
    """Linux eBPF SOCKMAP / TProxy Redirection Simulator"""
    def __init__(self):
        self.method = "None"
        self.latency_baseline = 35.0  # us
        self.cpu_baseline = 18.0     # %

    def configure_redirection(self, enabled=False, method="TProxy"):
        if not enabled:
            self.method = "None"
        else:
            self.method = method if method in ["TProxy", "SOCKMAP"] else "TProxy"

    def send_packet(self, size_kb=10):
        if self.method == "SOCKMAP":
            # Direct socket redirect, bypassing protocol stack
            latency = 2.0 + (size_kb * 0.1)
            cpu = 0.5
        elif self.method == "TProxy":
            # Standard transparent proxy interception
            latency = 12.0 + (size_kb * 0.5)
            cpu = 4.5
        else:
            # Traditional kernel protocol stack
            latency = self.latency_baseline + (size_kb * 1.5)
            cpu = self.cpu_baseline + (size_kb * 0.2)
        
        return {
            "status": "success",
            "method": self.method,
            "latency_us": round(latency, 2),
            "cpu_softirq_percent": round(cpu, 2),
            "bytes_transmitted": size_kb * 1024
        }


class LsmCompactionGym:
    """LSM Storage Engine Compaction Analyzer"""
    def __init__(self):
        self.levels = {0: [], 1: [], 2: []}
        self.write_amp = 1.0

    def write_batch(self, size_mb=64):
        self.levels[0].append(f"sstable-{len(self.levels[0])}-size-{size_mb}mb")
        self.write_amp += 1.0

    def trigger_compaction(self, level=0):
        if level not in self.levels or not self.levels[level]:
            return {"status": "error", "message": f"Level {level} has no SSTables to compact."}
        
        # Simulating merging files
        compacted_files = self.levels[level]
        self.levels[level] = []
        next_level = level + 1
        if next_level in self.levels:
            self.levels[next_level].append(f"compacted-from-L{level}")
            self.write_amp += len(compacted_files) * 0.5
            return {
                "status": "success",
                "message": f"Compacted {len(compacted_files)} files from L{level} to L{next_level}",
                "write_amplification": round(self.write_amp, 2)
            }
        return {"status": "error", "message": "Max level reached."}

    def get_stats(self):
        return {
            "write_amplification": round(self.write_amp, 2),
            "sstable_counts": {f"L{l}": len(files) for l, files in self.levels.items()}
        }


class RaftConsensusGym:
    """Raft Consensus / Leader Election Gym"""
    def __init__(self, num_nodes=3):
        self.nodes = [f"node_{i}" for i in range(num_nodes)]
        self.leader = "node_0"
        self.term = 1
        self.partitions = []

    def trigger_network_partition(self, split_nodes):
        # e.g., [['node_0'], ['node_1', 'node_2']]
        self.partitions = split_nodes
        # Check if leader is in the minority partition
        for part in self.partitions:
            if self.leader in part:
                if len(part) < len(self.nodes) / 2:
                    # Leader is isolated, step down
                    self.leader = None
                    self.term += 1
                    return {"status": "success", "message": "Leader partitioned in minority, stepped down. Election triggered."}
        return {"status": "success", "message": "Partition created.", "leader": self.leader}

    def request_vote(self, candidate_node):
        # Verify if node has majority partition
        for part in self.partitions:
            if candidate_node in part:
                if len(part) >= len(self.nodes) / 2:
                    self.leader = candidate_node
                    return {"status": "success", "message": f"{candidate_node} elected as leader of term {self.term}"}
        # If no partition configured, node wins by default
        if not self.partitions:
            self.leader = candidate_node
            return {"status": "success", "message": f"{candidate_node} elected as leader of term {self.term}"}
        return {"status": "error", "message": "Failed to win majority vote."}


class BorrowCheckerGym:
    """Rust MIR Borrow Checker Simulator"""
    def __init__(self):
        pass

    def submit_code(self, mir_statements):
        """
        Simulates parsing a subset of Rust-like borrow statements.
        statements: list of strings (e.g. ['let mut x = 5', 'let y = &x', 'let z = &mut x'])
        """
        borrows = {}  # var -> 'immut' or 'mut'
        for stmt in mir_statements:
            stmt = stmt.strip()
            if "let mut " in stmt:
                parts = stmt.split("let mut ")[1].split("=")
                var = parts[0].strip()
            elif "let " in stmt:
                parts = stmt.split("let ")[1].split("=")
                alias = parts[0].strip()
                expr = parts[1].strip()
                
                # Check for borrows
                if expr.startswith("&mut "):
                    ref_var = expr.split("&mut ")[1]
                    if ref_var in borrows:
                        return {
                            "status": "error",
                            "message": f"CompilationError: Cannot borrow `{ref_var}` as mutable because it is already borrowed as {borrows[ref_var]}."
                        }
                    borrows[ref_var] = "mut"
                elif expr.startswith("&"):
                    ref_var = expr.split("&")[1]
                    if ref_var in borrows and borrows[ref_var] == "mut":
                        return {
                            "status": "error",
                            "message": f"CompilationError: Cannot borrow `{ref_var}` as immutable because it is already borrowed as mutable."
                        }
                    borrows[ref_var] = "immut"
        return {"status": "success", "message": "MIR Borrow Checker passed successfully."}


class DailyDiagnosticsGym:
    """MySQL InnoDB Transaction Lock & CPU Scheduler Gym"""
    def __init__(self):
        pass

    def run_transaction(self, tx_id, keys_held, keys_requested):
        # Simple cycle detection for deadlocks
        # Simulate simple locking conflict
        for k in keys_requested:
            if k in keys_held:
                return {
                    "status": "error",
                    "message": f"DeadlockError: Transaction {tx_id} waiting on resource '{k}' held by another transaction. InnoDB deadlock engine aborted transaction."
                }
        return {"status": "success", "message": "Transaction locks acquired successfully."}
