# performance_monitor.py - Performance monitoring for ultra-fast automation
import time
import asyncio
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class PerformanceMetric:
    operation: str
    start_time: float
    end_time: float
    duration: float
    success: bool
    error: Optional[str] = None

class PerformanceMonitor:
    def __init__(self):
        self.metrics: List[PerformanceMetric] = []
        self.start_time = None
        self.current_operation = None
    
    def start_operation(self, operation: str):
        """Start timing an operation"""
        self.current_operation = operation
        self.start_time = time.time()
        print(f"⏱️ Starting: {operation}")
    
    def end_operation(self, success: bool = True, error: str = None):
        """End timing an operation"""
        if self.current_operation and self.start_time:
            end_time = time.time()
            duration = end_time - self.start_time
            
            metric = PerformanceMetric(
                operation=self.current_operation,
                start_time=self.start_time,
                end_time=end_time,
                duration=duration,
                success=success,
                error=error
            )
            
            self.metrics.append(metric)
            
            status = "✅" if success else "❌"
            print(f"{status} {self.current_operation}: {duration:.2f}s")
            
            self.current_operation = None
            self.start_time = None
    
    def get_total_time(self) -> float:
        """Get total execution time"""
        if not self.metrics:
            return 0.0
        
        first_start = min(m.start_time for m in self.metrics)
        last_end = max(m.end_time for m in self.metrics)
        return last_end - first_start
    
    def get_operation_time(self, operation: str) -> float:
        """Get time for specific operation"""
        for metric in self.metrics:
            if metric.operation == operation:
                return metric.duration
        return 0.0
    
    def get_slowest_operations(self, limit: int = 5) -> List[PerformanceMetric]:
        """Get the slowest operations"""
        sorted_metrics = sorted(self.metrics, key=lambda x: x.duration, reverse=True)
        return sorted_metrics[:limit]
    
    def get_failed_operations(self) -> List[PerformanceMetric]:
        """Get failed operations"""
        return [m for m in self.metrics if not m.success]
    
    def print_summary(self):
        """Print performance summary"""
        print("\n" + "="*50)
        print("📊 PERFORMANCE SUMMARY")
        print("="*50)
        
        total_time = self.get_total_time()
        print(f"⏱️ Total Time: {total_time:.2f} seconds")
        
        if total_time > 25:
            print(f"⚠️ Target: <25 seconds (Over by {total_time - 25:.2f}s)")
        else:
            print(f"🎉 Target: <25 seconds (Under by {25 - total_time:.2f}s)")
        
        print(f"\n📈 Operations: {len(self.metrics)}")
        successful = len([m for m in self.metrics if m.success])
        failed = len([m for m in self.metrics if not m.success])
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        
        if self.metrics:
            avg_time = sum(m.duration for m in self.metrics) / len(self.metrics)
            print(f"📊 Average operation time: {avg_time:.2f}s")
        
        # Show slowest operations
        slowest = self.get_slowest_operations(3)
        if slowest:
            print(f"\n🐌 Slowest Operations:")
            for i, metric in enumerate(slowest, 1):
                status = "✅" if metric.success else "❌"
                print(f"  {i}. {metric.operation}: {metric.duration:.2f}s {status}")
        
        # Show failed operations
        failed_ops = self.get_failed_operations()
        if failed_ops:
            print(f"\n❌ Failed Operations:")
            for metric in failed_ops:
                print(f"  - {metric.operation}: {metric.error}")
        
        print("="*50)
    
    def export_metrics(self, filename: str = "performance_metrics.txt"):
        """Export metrics to file"""
        with open(filename, 'w') as f:
            f.write("Performance Metrics Report\n")
            f.write("="*30 + "\n\n")
            
            for metric in self.metrics:
                status = "SUCCESS" if metric.success else "FAILED"
                f.write(f"{metric.operation}: {metric.duration:.2f}s [{status}]\n")
                if metric.error:
                    f.write(f"  Error: {metric.error}\n")
                f.write("\n")
            
            f.write(f"\nTotal Time: {self.get_total_time():.2f}s\n")
            f.write(f"Target: <25s\n")
            f.write(f"Performance: {'✅ MET' if self.get_total_time() <= 25 else '❌ MISSED'}\n")

# Global monitor instance
monitor = PerformanceMonitor()

def track_operation(operation: str):
    """Decorator to track operation performance"""
    def decorator(func):
        async def wrapper(*args, **kwargs):
            monitor.start_operation(operation)
            try:
                result = await func(*args, **kwargs)
                monitor.end_operation(success=True)
                return result
            except Exception as e:
                monitor.end_operation(success=False, error=str(e))
                raise
        return wrapper
    return decorator 