import ActiveScan
import PassiveScan
import Cloud

def main():
    while True:
        print("Choose an option:")
        print("1. Active Scan")
        print("2. Passive Scan")
        print("3. Cloud Scan")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            # Call active scan function
            ActiveScan.main()
        elif choice == '2':
            # Call passive scan function
            PassiveScan.main()
        elif choice == '3':
            # Call cloud scan function
            Cloud.main()
        elif choice == '4':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
