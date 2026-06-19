# Hardcore Systems Engineering: Interactive Sandboxes & Systems Gym

This repository provides visual cheatsheets, 10 standalone offline interactive sandboxes, and a B2B Systems Gym for training coding AI agents.

## 🌟 Key Features

1. **10 Standalone Offline Interactive Sandboxes (Explicit State)**:
   * Explore complex system designs (e.g., eBPF SOCKMAP redirection, LSM compaction, Raft consensus, Consistent Hashing) directly in your browser.
   * Low-saturation Morandi color palette designed for high aesthetic appeal and long reading comfort.
   * 100% self-contained single HTML files—no external dependencies, no server config. Just double-click to play!
   
2. **FDE Compiler Self-Healing Script**:
   * A Python backpropagation implementation demonstrating how to dynamically optimize AI Agent tool descriptions (docstrings) based on compilation tracebacks and schema errors.

3. **Headless Systems Gym (Implicit State)**:
   * OpenAI-Gym-style Python APIs representing complex systems, designed specifically for AI Agents and Reinforcement Learning (RL) agents to learn system diagnostics, performance optimization, and SRE incident response.

---

## 📂 Repository Structure

* `interactive_sandboxes/`: Stands as the home of our 10 visual HTML simulators.
* `fde_compiler_heal/`: Self-healing prompts and automatic docstring tuning script.
* `headless_gym/`: Systems Gym API for AI Agent training.

---

## 🛠️ How to Use

### 1. Visual Sandboxes (For Humans)
Go to the `interactive_sandboxes/` directory, choose any `.html` file (e.g., `tokio.html`), and open it in any web browser. Use the sliders and interactive buttons to simulate task stealing, thread scheduling, or consistent hashing load balance standard deviations.

### 2. Headless Systems Gym (For AI Agents)
Initialize the gym in Python to run headless simulations:

```python
from headless_gym.systems_gym import ConsistentHashGym

# Initialize consistent hash simulator
gym = ConsistentHashGym(num_nodes=3, vnodes=10)
gym.add_node("node_D")
result = gym.get_stats()
print(f"Load balance standard deviation: {result['std_dev']}")
```

---

## 📄 License & Commercial Inquiry

This project is dual-licensed under the **MIT License** and a **Commercial AI Training License**. 
* **Personal & Educational Use**: Free under MIT.
* **Commercial AI Model Training / Benchmark Use**: Requires a commercial license. For inquiries, please contact: `license@hardcoresystems.io`
