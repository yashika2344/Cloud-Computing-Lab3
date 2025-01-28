from locust import task, run_single_user, FastHttpUser
from insert_product import login

class AddToCartUser(FastHttpUser):
    host = "http://localhost:5000"
    
    def on_start(self):
        """
        This method runs at the start of the user's session.
        It logs in the user and retrieves the token for authenticated requests.
        """
        self.username = "test123"
        self.password = "test123"
        cookies = login(self.username, self.password)
        self.token = cookies.get("token") if cookies else None
        if not self.token:
            raise Exception("Failed to retrieve token during login")

    @task
    def view_cart(self):
        """
        Task to fetch the cart page.
        Authenticates with the token and provides additional headers.
        """
        headers = {
            "Accept": (
                "text/html,application/xhtml+xml,application/xml;q=0.9,"
                "image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8"
            ),
            "Cookie": f"token={self.token}",
            "Referer": "http://localhost:5000/product/1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }

        with self.client.get(
            "/cart",
            headers=headers,
            catch_response=True,
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed to load cart page with status code {response.status_code}")


if __name__ == "__main__":
    run_single_user(AddToCartUser)
