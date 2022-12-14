from django.urls import reverse

from WePay.models.bill import Topic
from .setUp import BaseSetUp
from ..models import Bills
from unittest import skip
from .utlis import create_user, create_topic, add_user_topic


class BaseViewTest(BaseSetUp):
    def setUp(self):
        """Setup before running a tests."""
        super(BaseViewTest, self).setUp()
        self.test_header = create_user(username="test_header", password="header123", email="test@example.com")
        self.client.force_login(self.test_header.user)

    def test_logout(self):
        """After logout bring user back to login page."""
        response = self.client.post("/accounts/logout/")
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)


class BillViewTest(BaseViewTest):
    """Test for BillView"""

    def setUp(self):
        """Setup before running a tests."""
        super(BillViewTest, self).setUp()

    def test_bill_page(self):
        """After login its will goes to bill page."""
        response = self.client.get("/bill/")
        self.assertEqual(response.status_code, 200)

    def test_uncreated_bill(self):
        """test redirect and error if user has uncreated bill."""
        pass


class BillCreateViewTest(BaseViewTest):
    """Test for BillCreateView"""

    def setUp(self):
        """Setup before running a tests."""
        super(BillCreateViewTest, self).setUp()

    def test_navigate_create_bill_page(self):
        """test navigate to bill page"""
        response = self.client.get("/bill/create/")
        self.assertEqual(response.status_code, 200)

    def test_create_bill(self):
        """test created bill."""
        self.assertEqual(Bills.objects.get(pk=1), self.bill)  # create success

    @skip("Its not work.")
    def test_create_only_initial_topic(self):
        """test create a bill with initial topic."""
        self.new_bill = Bills.objects.create(
            header=self.user_profile, name="Beverage(s)"
        )
        self.est = Topic.objects.create(title="Est", price=20, bill=self.new_bill)
        self.est.add_user(self.user1)
        self.est.add_user(self.user2)
        self.new_bill.add_topic(self.est)
        self.assertEqual(Bills.objects.get(pk=2), self.new_bill)
        self.assertEqual(Bills.objects.get(pk=2).name, self.new_bill.name)
        self.assertEqual(Topic.objects.get(pk=3).title, self.est.title)
        self.assertEqual(Topic.objects.get(pk=3).price, self.est.price)
        self.assertEqual(Bills.objects.get(pk=2).all_user, [self.user1, self.user2])
        self.client.post(reverse("bills:create"))
        self.client.post(reverse("bills:success", kwargs={"pk": 2}))
        self.assertTrue(Bills.objects.get(pk=2).is_created)

    def test_response_with_create_bill(self):
        """Test create bill with response"""
        data = {
            "title": "Est",
            "topic_name": "Toast",
            "username[]": [self.user1, self.user2],
            "topic_price": 2000,
        }
        response = self.client.post(reverse("bills:create"), data=data)
        bill = Bills.objects.last()
        self.assertFalse(bill.is_created)
        self.assertEqual(response["Location"], "/bill/2/add")  # POST success
        response2 = self.client.get(reverse("bills:success", kwargs={"pk": 2}))
        self.assertEqual(
            response2["Location"], "/bill/"
        )  # After success redirect to bill page
        self.assertRedirects(response2, "/bill/", 302, 200)
        bills = Bills.objects.get(pk=2)
        topic = Topic.objects.get(title="Toast")
        self.assertTrue(bills.is_created)
        self.assertEqual(bills.name, "Est")
        self.assertEqual(topic.title, "Toast")
        self.assertEqual(list(topic.user.all()), [self.user1, self.user2])
        self.assertEqual(topic.price, 2000)
        self.assertEqual(bills.total_price, 2000)

    def test_create_bill_with_more_topic(self):
        """test create a bill with initial topic and add more topic."""
        self.new_bill = Bills.objects.create(
            header=self.test_header, name="Beverage(s)"
        )
        self.est = create_topic(title="Est", price=20, bill=self.new_bill)
        add_user_topic(self.est, [self.user1, self.user2])
        self.fanta = Topic.objects.create(title="Fanta", price=30, bill=self.new_bill)
        add_user_topic(self.fanta, [self.user1, self.user2, self.user3])
        self.assertEqual(Bills.objects.get(pk=2), self.new_bill)
        self.assertEqual(Bills.objects.get(pk=2).name, self.new_bill.name)
        self.assertEqual(Topic.objects.get(pk=3).title, self.est.title)
        self.assertEqual(Topic.objects.get(pk=4).title, self.fanta.title)
        self.assertEqual(
            Bills.objects.get(pk=2).all_user, [self.user1, self.user2, self.user3]
        )
        self.assertEqual(self.new_bill.total_price, 50)
        self.client.post(reverse("bills:success", kwargs={"pk": 2}))
        self.assertTrue(Bills.objects.get(pk=2).is_created)

    def test_close_bill(self):
        """test close bill."""
        pass

    def test_delete_bill(self):
        """test delete bill."""
        self.client.post(reverse("bills:delete", kwargs={"pk": 1}))
        self.assertFalse(Bills.objects.get(pk=1).is_created)


class DetailViewTest(BaseViewTest):
    def setUp(self):
        """Setup before running a tests."""
        super(DetailViewTest, self).setUp()

    @skip("Can't get bill that was created.")
    def test_navigation(self):
        """test navigation after bill object has created"""
        response = self.client.get("/bill/1/")
        self.assertEqual(response.status_code, 302)

    def test_bill_not_exist(self):
        """test navigation if go to bill that does not exist it will 404"""
        response = self.client.get(reverse("bills:detail", kwargs={"pk": 1000}))
        self.assertEqual(response.status_code, 404)


class AddTopicView(BaseViewTest):
    def test_add_topic(self):
        data = {
            "title": "Est",
            "topic_name": "Toast",
            "username[]": [self.user1, self.user2],
            "topic_price": 2000,
        }
        data2 = {
            "topic_name": "Toasting",
            "username[]": [self.user1, self.user2, self.user3],
            "topic_price": 3000,
        }
        data3 = {
            "topic_name": "Tea",
            "username[]": [self.user2, self.user3],
            "topic_price": 4000,
        }
        response = self.client.post(reverse("bills:create"), data=data)
        self.assertFalse(Bills.objects.last().is_created)
        self.assertRedirects(response, "/bill/2/add", 302)
        response2 = self.client.post(reverse("bills:add", kwargs={"pk": 2}), data=data2)
        self.assertRedirects(response2, "/bill/2/add", 302)  # POST Success Reload Page
        # Check that bill is not created when add topic
        self.assertFalse(Bills.objects.last().is_created)
        response3 = self.client.post(reverse("bills:add", kwargs={"pk": 2}), data=data3)
        self.assertRedirects(response3, "/bill/2/add", 302)  # POST Success Reload Page
        # Check that bill is not created when add topic
        self.assertFalse(Bills.objects.last().is_created)
        response4 = self.client.get(reverse("bills:success", kwargs={"pk": 2}))
        self.assertRedirects(response4, "/bill/", 302)  # POST Success
        self.assertTrue(Bills.objects.get(pk=2).is_created)  # Bill is created.
        # Checked Value in Bill.
        this_bill = Bills.objects.get(pk=2)
        first_topic = Topic.objects.get(bill=this_bill, title="Toast")
        second_topic = Topic.objects.get(bill=this_bill, title="Toasting")
        third_topic = Topic.objects.get(bill=this_bill, title="Tea")
        bill_data = {
            "title": this_bill.name,
            "topic_name": first_topic.title,
            "username[]": list(first_topic.user.all()),
            "topic_price": first_topic.price,
        }
        topic_data1 = {
            "topic_name": second_topic.title,
            "username[]": list(second_topic.user.all()),
            "topic_price": second_topic.price,
        }
        topic_data2 = {
            "topic_name": third_topic.title,
            "username[]": list(third_topic.user.all()),
            "topic_price": third_topic.price,
        }
        self.assertDictEqual(data, bill_data)
        self.assertDictEqual(data2, topic_data1)
        self.assertDictEqual(data3, topic_data2)
