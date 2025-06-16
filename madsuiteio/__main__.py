import madsuiteio
import argparse

def main():
    parser = argparse.ArgumentParser(description="Build, run, and deploy MadSuiteIO server")
    parser.add_argument("action", choices=["build", "serve", "deploy"], help="Action to perform: build, serve, or deploy")
    args = parser.parse_args()

    if args.action == "build":
        madsuiteio.build()
    elif args.action == "serve":
        madsuiteio.serve()
    elif args.action == "deploy":
        madsuiteio.deploy()
        
if __name__ == "__main__":
    main()
