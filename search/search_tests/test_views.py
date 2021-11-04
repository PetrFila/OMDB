import json
from unittest import mock

from django.test import TransactionTestCase

from search.models import Title


class SearchViewTestCase(TransactionTestCase):
    """Tests that the search view works correcly """

    def setUp(self):

        self.example_omdb_api_response = (
            b'{"Title":"Disco","Year":"2008","Rated":"N/A","Released":"02 Apr 2008",'
            b'"Runtime":"103 min","Genre":"Comedy, Music","Director":"Fabien Onteniente",'
            b'"Writer":"Fabien Onteniente, Philippe Guillard, Franck Dubosc",'
            b'"Actors":"Franck Dubosc, Emmanuelle B\xc3\xa9art, G\xc3\xa9rard Depardieu",'
            b'"Plot":"Didier Travolta (Franck Dubosc) is a 40-year-old disco music fan who has'
            b' no job, lives with his mother, and has a son he hasn\'t seen for a while in '
            b'Britain. The mother of his son refuses to send him their son for the holidays'
            b' unless he can offer him a real vacation, not just going to bars of the French'
            b' port city of Le Havre. As the jobless Didier has no money, the only way he can'
            b' see his son is by winning a dance contest organized by his friend Jackson '
            b'(G\xc3\xa9rard Depardieu), with the prize a vacation to Australia for two. Didier'
            b' persuades his two former dancing buddies (Samuel Le Bihan and Abbes Zahmani) to'
            b' get the once-famous \\"Bee Kings\\" group back on the dancefloor. Years have passed'
            b' and they need a dance coach (Emmanuelle B\xc3\xa9art) to get them ready for the'
            b' competition. They soon find out that even if they once were the best, times have'
            b' changed. Jobs, wives, love, ridiculous looks, old-fashioned clothes, talented '
            b'contestants... Can they reclaim their past disco glory?","Language":"French",'
            b'"Country":"France","Awards":"N/A",'
            b'"Poster":"https://m.media-amazon.com/images/M/MV5BMTU1MjI0MzgwM15BMl5BanBnXkFtZTcwNjA'
            b'5MjI3MQ@@._V1_SX300.jpg","Ratings":[{"Source":"Internet Movie Database","Value":"4.3/10"}],'
            b'"Metascore":"N/A","imdbRating":"4.3","imdbVotes":"1,518","imdbID":"tt0953369","Type":"movie",'
            b'"DVD":"05 Feb 2015","BoxOffice":"N/A","Production":"N/A","Website":"N/A","Response":"True"}'
        )

        self.title1 = Title.objects.create(
            title="So unique",
            type="movie",
            year="2021",
            genre="Test",
            director="Luke",
            actor="Luke as someone else",
            plot="Thickens",
            image_link="http://example.com/image.jpg",
            IMDB_link="https://www.imdb.com/title/tt0944947/"
        )

        self.title1 = Title.objects.create(
            title="Individual",
            type="series",
            year="2021",
            genre="Test",
            director="Luke",
            actor="Luke as someone else",
            plot="Thickens",
            image_link="http://example.com/image.jpg",
            IMDB_link="https://www.imdb.com/title/tt0944947/"
        )

    def test_find_title(self):
        """Tests that OMDB is called when no local titles found"""

        with mock.patch("search.views.get_title_from_OMDB") as mock_OMDB:
            mock_OMDB.return_value = json.loads(self.example_omdb_api_response)

            # Call the test endpoint with django test framework
            response = self.client.post("/result/", {"title": "Disco"})

            # There should have been no match for any local titles
            # And the OMDB api should have been called
            mock_OMDB.assert_called()

            # We should have the title in the database now
            new_title = Title.objects.get(title="Disco")

            self.assertEqual("movie", new_title.type)
            self.assertEqual("2008", new_title.year)
            self.assertEqual("Comedy, Music", new_title.genre)

            # etc

            response_body = response.content.decode()
            # test some attributes of the template response
            self.assertIn("This is what I found", response_body)

            # Check that the message about searching in OMDB was added
            self.assertEqual(1, len(response.context['messages']))

            # likely much better ways to access this
            self.assertEqual(
                "Title found in the OMDB and has been added to the local database.",
                [i for i in response.context['messages']][0].message
            )
