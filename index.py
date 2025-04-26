import tkinter as tk
from tkinter import messagebox
from collections import deque
import time

class CodeCrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Cracker")
        self.root.geometry("400x300")
        
        # Target code 
        self.target_code = "1234" # default 
        self.attempts = 0
        self.start_time = 0
        
        # GUI Elements
        self.label = tk.Label(root, text="Enter 4-digit code (or use default '1234'):")
        self.label.pack(pady=10)
        
        self.code_entry = tk.Entry(root, width=10)
        self.code_entry.pack(pady=5)
        
        self.start_button = tk.Button(root, text="Start Cracking", command=self.start_cracking)
        self.start_button.pack(pady=10)
        
        self.status_label = tk.Label(root, text="Status: Waiting to start")
        self.status_label.pack(pady=10)
        
        self.result_label = tk.Label(root, text="")
        self.result_label.pack(pady=5)
        
        self.attempts_label = tk.Label(root, text="Attempts: 0")
        self.attempts_label.pack(pady=5)
        
        self.time_label = tk.Label(root, text="Time: 0.0s")
        self.time_label.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_cracking, state=tk.DISABLED)
        self.stop_button.pack(pady=10)
        
        self.running = False
        
    def check_code(self, code):
        """Check if the guessed code matches the target code."""
        return code == self.target_code
    
    # Implement BFS algo
    def bfs_crack(self):
        """Implement BFS to crack the 4-digit code."""
        queue = deque(['0000'])
        visited = set(['0000'])
        self.attempts = 0
        
        while queue and self.running:
            current_code = queue.popleft()
            self.attempts += 1
            
            # Update GUI
            self.attempts_label.config(text=f"Attempts: {self.attempts}")
            self.result_label.config(text=f"Trying: {current_code}")
            self.time_label.config(text=f"Time: {(time.time() - self.start_time):.1f}s")
            self.root.update()
            
            if self.check_code(current_code):
                return current_code
            
            # Generate next possible codes (change one digit at a time)
            for i in range(4):
                current_digits = list(current_code)
                current_digit = int(current_digits[i])
                
                # Try increment and decrement of current digit
                for delta in [-1, 1]:
                    new_digit = (current_digit + delta) % 10
                    current_digits[i] = str(new_digit)
                    new_code = ''.join(current_digits)
                    
                    if new_code not in visited:
                        visited.add(new_code)
                        queue.append(new_code)
                        
            # Small delay to make GUI updates visible
            time.sleep(0.01)
        
        return None
    
    def start_cracking(self):
        """Start the code cracking process."""
        if not self.running:
            # Get target code from entry or use default
            user_code = self.code_entry.get()
            if user_code and user_code.isdigit() and len(user_code) == 4:
                self.target_code = user_code
            else:
                self.target_code = "1234"
                
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="Status: Cracking...")
            self.start_time = time.time()
            
            # Run BFS
            result = self.bfs_crack()
            
            if result and self.running:
                self.status_label.config(text="Status: Success!")
                self.result_label.config(text=f"Code found: {result}")
                messagebox.showinfo("Success", f"Code cracked: {result}\nAttempts: {self.attempts}\nTime: {(time.time() - self.start_time):.1f}s")
            elif not self.running:
                self.status_label.config(text="Status: Stopped")
                self.result_label.config(text="Cracking stopped")
            else:
                self.status_label.config(text="Status: Failed")
                self.result_label.config(text="No solution found")
                
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
    
    def stop_cracking(self):
        """Stop the cracking process."""
        self.running = False

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeCrackerApp(root)
    root.mainloop()