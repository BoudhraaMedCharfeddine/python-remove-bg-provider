#!/usr/bin/env python3
"""
Load testing script for Python Remove Background Provider
"""

import asyncio
import aiohttp
import time
import argparse
from pathlib import Path
from PIL import Image
import io
import statistics


async def create_test_image():
    """Create a test image for load testing"""
    img = Image.new('RGB', (200, 200), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes


async def make_request(session, url, image_data):
    """Make a single request to the background removal endpoint"""
    start_time = time.time()
    
    data = aiohttp.FormData()
    data.add_field('file', image_data, filename='test.png', content_type='image/png')
    
    try:
        async with session.post(url, data=data) as response:
            result = await response.read()
            end_time = time.time()
            
            return {
                'status_code': response.status,
                'response_time': end_time - start_time,
                'response_size': len(result),
                'success': response.status == 200
            }
    except Exception as e:
        end_time = time.time()
        return {
            'status_code': 0,
            'response_time': end_time - start_time,
            'response_size': 0,
            'success': False,
            'error': str(e)
        }


async def run_load_test(base_url, concurrent_users, total_requests, endpoint='/bg/remove'):
    """Run load test with specified parameters"""
    url = f"{base_url}{endpoint}"
    
    # Create test image
    image_data = await create_test_image()
    
    print(f"🚀 Starting load test:")
    print(f"   URL: {url}")
    print(f"   Concurrent users: {concurrent_users}")
    print(f"   Total requests: {total_requests}")
    print(f"   Requests per user: {total_requests // concurrent_users}")
    print()
    
    # Create semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(concurrent_users)
    
    async def limited_request(session):
        async with semaphore:
            return await make_request(session, url, image_data.getvalue())
    
    # Start timing
    start_time = time.time()
    
    # Create session and run requests
    async with aiohttp.ClientSession() as session:
        tasks = [limited_request(session) for _ in range(total_requests)]
        results = await asyncio.gather(*tasks)
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Analyze results
    successful_requests = [r for r in results if r['success']]
    failed_requests = [r for r in results if not r['success']]
    
    if successful_requests:
        response_times = [r['response_time'] for r in successful_requests]
        avg_response_time = statistics.mean(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        p95_response_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        p99_response_time = statistics.quantiles(response_times, n=100)[98]  # 99th percentile
        
        avg_response_size = statistics.mean([r['response_size'] for r in successful_requests])
    else:
        avg_response_time = min_response_time = max_response_time = 0
        p95_response_time = p99_response_time = 0
        avg_response_size = 0
    
    requests_per_second = len(successful_requests) / total_time if total_time > 0 else 0
    
    # Print results
    print("📊 Load Test Results:")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Successful requests: {len(successful_requests)}")
    print(f"   Failed requests: {len(failed_requests)}")
    print(f"   Success rate: {(len(successful_requests)/total_requests)*100:.1f}%")
    print(f"   Requests per second: {requests_per_second:.2f}")
    print()
    
    if successful_requests:
        print("⏱️  Response Times:")
        print(f"   Average: {avg_response_time:.3f}s")
        print(f"   Minimum: {min_response_time:.3f}s")
        print(f"   Maximum: {max_response_time:.3f}s")
        print(f"   95th percentile: {p95_response_time:.3f}s")
        print(f"   99th percentile: {p99_response_time:.3f}s")
        print()
        
        print("📦 Response Sizes:")
        print(f"   Average: {avg_response_size:.0f} bytes")
        print()
    
    if failed_requests:
        print("❌ Failed Requests:")
        error_counts = {}
        for req in failed_requests:
            error = req.get('error', f"HTTP {req['status_code']}")
            error_counts[error] = error_counts.get(error, 0) + 1
        
        for error, count in error_counts.items():
            print(f"   {error}: {count} requests")
        print()
    
    # Performance thresholds
    print("🎯 Performance Analysis:")
    if requests_per_second >= 10:
        print("   ✅ Requests per second: GOOD")
    elif requests_per_second >= 5:
        print("   ⚠️  Requests per second: ACCEPTABLE")
    else:
        print("   ❌ Requests per second: POOR")
    
    if avg_response_time <= 2.0:
        print("   ✅ Average response time: GOOD")
    elif avg_response_time <= 5.0:
        print("   ⚠️  Average response time: ACCEPTABLE")
    else:
        print("   ❌ Average response time: POOR")
    
    if p95_response_time <= 5.0:
        print("   ✅ 95th percentile response time: GOOD")
    elif p95_response_time <= 10.0:
        print("   ⚠️  95th percentile response time: ACCEPTABLE")
    else:
        print("   ❌ 95th percentile response time: POOR")


def main():
    parser = argparse.ArgumentParser(description='Load test the Python Remove Background Provider')
    parser.add_argument('--url', default='http://localhost:8001', help='Base URL of the service')
    parser.add_argument('--users', type=int, default=5, help='Number of concurrent users')
    parser.add_argument('--requests', type=int, default=50, help='Total number of requests')
    parser.add_argument('--endpoint', default='/bg/remove', help='Endpoint to test')
    
    args = parser.parse_args()
    
    print("🧪 Python Remove Background Provider - Load Test")
    print("=" * 50)
    
    try:
        asyncio.run(run_load_test(args.url, args.users, args.requests, args.endpoint))
    except KeyboardInterrupt:
        print("\n🛑 Load test interrupted by user")
    except Exception as e:
        print(f"\n❌ Load test failed: {e}")


if __name__ == '__main__':
    main()





