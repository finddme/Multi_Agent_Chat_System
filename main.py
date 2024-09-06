import argparse
import six, os, torch
from app.app import app
import asyncio

async def main(args):
    await app(args)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--image', type=str, default='endpoint', choices=["endpoint","model","none"],required=False)
    parser.add_argument('--final-grader', type=str, default='none', choices=["model","hitl","none"], required=False)
    parser.add_argument('--ai-db-restore', type=str, default='no', choices=["yes","no"], required=False)

    args = parser.parse_args()

    asyncio.run(main(args))




    
