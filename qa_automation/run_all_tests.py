from testcases.test_case_1_search import test_amazon_search
from testcases.test_case_2_cart import test_flipkart_cart
from testcases.test_case_3_apple_form import test_apple_form

def run_all_tests():
    print("Running Test Case 1: Search & Product Validation")
    test_amazon_search()
    
    print("\nRunning Test Case 2: Cart Functionality")
    test_flipkart_cart()

    print("\nRunning Test Case 3: Apple Form Validation")
    test_apple_form()

if __name__ == "__main__":
    run_all_tests()
