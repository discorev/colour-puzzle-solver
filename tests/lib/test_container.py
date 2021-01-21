"""Test the contianer module."""
from unittest import TestCase, expectedFailure
from solver.lib.container import Container
from solver.lib.item import Item
from solver.lib.colour import Colour


class TestContainer(TestCase):
    """Test cases for the container class."""

    def test_empty_container(self):
        """Construct an empty container and check it's properties."""
        cont = Container([])
        self.assertEqual(cont.capacity, 4, "Capacity should be 4")
        self.assertTrue(cont.is_empty, "An empty container is empty")
        self.assertFalse(cont.is_full, "An empty container is not full")
        self.assertTrue(cont.is_unique, "An empty container is unique")
        self.assertTrue(cont.is_solved, "An empty container is solved")
        self.assertEqual(len(cont), 0, "An empty container has length 0")
        self.assertTrue(
            cont.test(Item(Colour.RED)), "Any colour should test true"
        )
        self.assertTrue(
            cont.test(Item(Colour.BLUE)), "Any colour should test true"
        )
        self.assertEqual(str(cont), "[    ]", "Empty collection")
        self.assertEqual(cont.__repr__(), "[]", "Empty collection")

    def test_container_capacity(self):
        """Check changing the capacity works."""
        cont = Container(["GREEN"], 2)
        self.assertEqual(cont.capacity, 2, "Container capactiy is two")
        self.assertFalse(cont.is_full, "Container is not full")
        self.assertEqual(
            str(cont),
            "[\x1b[38;2;102;153;0m■\x1b[39m ]",
            "Container only shows one block",
        )
        self.assertTrue(cont.add(Item(Colour.GREEN)), "Add should succeed")
        self.assertTrue(cont.is_full, "Container is now full")
        self.assertTrue(cont.is_unique, "Container is unique")
        self.assertTrue(cont.is_solved, "Container is solved")
        self.assertEqual(
            str(cont),
            "[\x1b[38;2;102;153;0m■\x1b[39m\x1b[38;2;102;153;0m■\x1b[39m]",
            "Container shows two blocks",
        )

    def test_container_from_container_with_different_capacity(self):
        """Construct a container from a container with a different capactiy."""
        large_container = Container(["RED", "RED", "RED", "RED"])
        small_container = Container(large_container, 2)
        self.assertEqual(
            len(small_container),
            2,
            "Container should be constrained to maximum capacity",
        )
        self.assertTrue(
            small_container.is_full,
            "Container should be full after construction",
        )

    def test_container_from_item_sequence(self):
        """Construct a container with a sequence of items."""
        cont = Container([Item(Colour.RED), Item(Colour.GREEN)])
        self.assertTupleEqual(
            cont.data, (Colour.RED, Colour.GREEN), "Should match item colours"
        )

    def test_container_from_invalid_type(self):
        """Check that construction with a bad type raises an exception."""
        with self.assertRaises(TypeError):
            Container(None)

        with self.assertRaises(TypeError):
            Container(object)

    def test_container_full_mixed(self):
        """Construct a full mixed container and check it's properties."""
        cont = Container(["RED", "RED", "GREEN", "GREEN"])
        self.assertEqual(cont.capacity, 4, "Capacity should be 4")
        self.assertFalse(cont.is_empty)
        self.assertTrue(cont.is_full)
        self.assertFalse(cont.is_unique)
        self.assertFalse(cont.is_solved)
        self.assertEqual(cont.head, Colour.GREEN)
        self.assertFalse(
            cont.test(Item(Colour.RED)),
            "Test never passes for a full container",
        )
        self.assertFalse(
            cont.test(Item(Colour.GREEN)),
            "Test never passes for a full container",
        )
        self.assertEqual(
            str(cont),
            "[\x1b[31m■\x1b[39m\x1b[31m■\x1b[39m\x1b[38;2;102;153;0m■\x1b[39m"
            "\x1b[38;2;102;153;0m■\x1b[39m]",
            "Viewable representation",
        )
        self.assertEqual(
            cont.__repr__(),
            "['RED','RED','GREEN','GREEN']",
            "Copy pasteable representation",
        )

    def test_container_test_non_full(self):
        """Check the test method of a container."""
        cont = Container(["RED", "RED", "GREEN"])
        self.assertEqual(cont[-1], Colour.GREEN, "Head is green")
        self.assertTrue(cont.test(Item(Colour.GREEN)), "Head is green")
        self.assertFalse(cont.test(Item(Colour.RED)), "Head is not red")

    def test_container_add_empty(self):
        """Test adding to an empty container."""
        cont = Container([])
        self.assertTrue(cont.add(Colour.RED), "Add should succeed")
        self.assertFalse(cont.is_empty, "The container is no longer empty")
        self.assertTupleEqual(
            cont.data, (Colour.RED,), "Red has been added to the container"
        )

    def test_container_add_full(self):
        """Test adding to a full container."""
        cont = Container(["RED"], 1)
        self.assertTrue(cont.is_full, "The container is full")

        self.assertFalse(
            cont.add(Colour.RED), "Cannot add to a full container"
        )
        self.assertTupleEqual(
            cont.data, (Colour.RED,), "The collection should be unchanged"
        )

    def test_container_pour_single_to_empty(self):
        """Check pouring a single item to an empty container."""
        cont = Container(["RED"])
        target = Container([])
        self.assertTrue(cont.pour(target), "Pour should succeed.")
        self.assertEqual(len(cont), 0, "Container is now empty")
        self.assertTrue(cont.is_empty, "Container is now empty")
        self.assertEqual(len(target), 1, "Target now has the item")
        self.assertFalse(target.is_empty, "Target is no longer empty")
        self.assertTupleEqual(
            target.data, (Colour.RED,), "Target now has the red item"
        )

    def test_container_pour_from_empty(self):
        """Check pouring from an empty container."""
        cont = Container([])
        target = Container([])
        self.assertFalse(
            cont.pour(target), "Cannot poour from an empty container"
        )

    def test_container_pour_single_to_matching(self):
        """Check pouring a single item to an empty container."""
        cont = Container(["RED"])
        target = Container(["RED"])
        self.assertTrue(cont.pour(target), "Pour should succeed.")
        self.assertEqual(len(cont), 0, "Container is now empty")
        self.assertTrue(cont.is_empty, "Container is now empty")
        self.assertEqual(len(target), 2, "Target now has two items")
        self.assertTupleEqual(
            target.data,
            (Colour.RED, Colour.RED),
            "Target now has two red items",
        )

    def test_container_pour_single_to_non_matching(self):
        """Check pouring a single item to a container of a different colour."""
        cont = Container(["RED"])
        target = Container(["GREEN"])
        self.assertFalse(cont.pour(target), "Pour should fail.")
        self.assertEqual(len(cont), 1, "Container still has one item")
        self.assertEqual(
            cont.data, (Colour.RED,), "Container still has one red item"
        )
        self.assertEqual(len(target), 1, "Target still has one item")
        self.assertTupleEqual(
            target.data, (Colour.GREEN,), "Target still only has a green item"
        )

    def test_container_pour_single_to_full(self):
        """Check pouring into a full container."""
        cont = Container(["RED"])
        target = Container(["RED"], 1)
        self.assertFalse(cont.pour(target), "Pour should fail")
        self.assertEqual(len(cont), 1, "Container length should not change")
        self.assertEqual(len(target), 1, "Target length should not change")

    def test_container_pour_multiple_matching_to_empty(self):
        """Check pouring multiple matching items to an empty container."""
        cont = Container(["RED", "RED"])
        target = Container([])
        self.assertTrue(cont.pour(target), "Pour should succeed.")
        self.assertEqual(len(cont), 0, "Container is now empty")
        self.assertTrue(cont.is_empty, "Container is now empty")
        self.assertEqual(len(target), 2, "Target now has the item")
        self.assertFalse(target.is_empty, "Target is no longer empty")
        self.assertTupleEqual(
            target.data,
            (Colour.RED, Colour.RED),
            "Target now has the red item",
        )

    def test_container_pour_multiple_matching_to_matching(self):
        """Check pouring multiple matching items to a matching container."""
        cont = Container(["RED", "RED"])
        target = Container(["RED", "RED"])
        self.assertTrue(cont.pour(target), "Pour should succeed.")
        self.assertEqual(len(cont), 0, "Container is now empty")
        self.assertTrue(cont.is_empty, "Container is now empty")
        self.assertEqual(len(target), 4, "Target now has the item")
        self.assertTrue(target.is_full, "Target is now full")
        self.assertTupleEqual(
            target.data,
            (Colour.RED, Colour.RED, Colour.RED, Colour.RED),
            "Target now has the red items",
        )

    def test_container_pour_multiple_matching_to_matching_overflowing(self):
        """Check pouring multiple matching items to overfill a container."""
        cont = Container(["RED", "RED"])
        target = Container(["RED", "RED", "RED"])
        self.assertTrue(cont.pour(target), "Pour should succeed.")
        self.assertEqual(len(cont), 1, "Container still has one item")
        self.assertTupleEqual(
            cont.data,
            (Colour.RED,),
            "Container still has a remaining red item",
        )
        self.assertEqual(len(target), 4, "Target now has four items")
        self.assertTrue(target.is_full, "Target is now full")
        self.assertTupleEqual(
            target.data,
            (Colour.RED, Colour.RED, Colour.RED, Colour.RED),
            "Target now has four red items",
        )

    def test_container_copy_and_mutate(self):
        """Check that copy results in a container that can be mutated."""
        cont = Container(["RED"])
        copy = cont.copy()
        self.assertEqual(cont, copy, "New container should equal the original")
        self.assertTrue(copy.add(Item(Colour.RED)), "Add should succeed")
        self.assertNotEqual(
            cont, copy, "The add should only affect one container"
        )

    def test_container_num_at_head(self):
        """Check the number of matches is initalised correctly."""
        cont = Container(["GREEN", "RED", "GREEN"])
        self.assertEqual(cont.num_matching_head, 1, "No consecutive colours")
        cont = Container(["GREEN", "GREEN"])
        self.assertEqual(cont.num_matching_head, 2, "Two consecutive colours")
        cont = Container([])
        self.assertEqual(cont.num_matching_head, 0, "Empty Container")

    def test_container_num_at_head_after_add(self):
        """Check the number of matches after an add is correct."""
        cont = Container(["GREEN", "RED", "GREEN"])
        self.assertEqual(cont.num_matching_head, 1, "No consecutive colours")
        cont.add(Colour.GREEN)
        self.assertEqual(
            cont.num_matching_head, 2, "Two consecutive colours after add"
        )

    def test_container_num_at_head_after_pour_single_in_src(self):
        """After pour check the number of matches is in both src and dest.

        In this test there should be a count of one in the src and two in the
        dest after the pour.
        """
        src = Container(["BLUE", "ORANGE", "RED", "GREEN"])
        dest = Container(["GREEN", "RED", "GREEN"])
        src.pour(dest)
        self.assertEqual(
            dest.num_matching_head,
            2,
            "Two consecutive colours in dest after pour",
        )
        self.assertEqual(
            src.num_matching_head,
            1,
            "No consecutive colours in non-empty src after pour",
        )

    def test_container_num_at_head_after_pour_multiple_in_src(self):
        """After pour check the number of matches is in both src and dest.

        In this test there should be a count of two in the src and dest after
        the pour
        """
        src = Container(["BLUE", "RED", "RED", "GREEN"])
        dest = Container(["GREEN", "RED", "GREEN"])
        src.pour(dest)
        self.assertEqual(
            dest.num_matching_head,
            2,
            "Two consecutive colours in dest after pour",
        )
        self.assertEqual(
            src.num_matching_head,
            2,
            "Two consecutive colours in src after pour",
        )

    def test_container_from_container_with_lower_capacity(self):
        """Test creating a new container from a smaller one.

        This test is currently expected to fail as the capacity is not
        maintained when a container is constructed from another.
        """
        original = Container(["RED"], 1)
        new = Container(original)
        self.assertTrue(new.is_full)
        self.assertTrue(new.is_solved)
        self.assertEqual(original, new)

    def test_container_equals_container(self):
        """Test creating a new container from a smaller one.

        This test is currently expected to fail as the capacity is not
        maintained when a container is constructed from another.
        """
        cont = Container(["GREEN", "RED", "GREEN"])
        self.assertEqual(cont, cont, "Container equals itself")
        self.assertEqual(
            cont,
            Container(["GREEN", "RED", "GREEN"]),
            "Container equals another instance with the same content",
        )
        self.assertNotEqual(
            cont,
            Container(["RED", "GREEN", "GREEN"]),
            "Container does not equal another instance with the same content "
            "in a different order",
        )

    def test_container_equals_sequence(self):
        """Test creating a new container from a smaller one.

        This test is currently expected to fail as the capacity is not
        maintained when a container is constructed from another.
        """
        cont = Container(["GREEN", "RED", "GREEN"])
        self.assertEqual(
            cont,
            ["GREEN", "RED", "GREEN"],
            "Container equals the same sequence",
        )
        self.assertNotEqual(
            cont,
            ["RED", "GREEN", "GREEN"],
            "Container does not equal a squence with the same content in a "
            "different order",
        )

    def test_container_not_equal_other(self):
        """Test creating a new container from a smaller one.

        This test is currently expected to fail as the capacity is not
        maintained when a container is constructed from another.
        """
        cont = Container(["GREEN", "RED", "GREEN"])
        self.assertNotEqual(
            cont,
            object(),
            "Comparison with non-sequence or container should always fail.",
        )

    def test_container_iter_and_next(self):
        """Test iterator and next."""
        cont = Container(["RED", "GREEN", "GREY", "BLUE"])
        iterator = iter(cont)
        self.assertTrue(next(iterator) == "BLUE")
        self.assertTrue(next(iterator) == "GREY")
        self.assertTrue(next(iterator) == "GREEN")
        self.assertTrue(next(iterator) == "RED")
        with self.assertRaises(StopIteration):
            next(iterator)
