from alembic_utils.pg_function import PGFunction
from alembic_utils.pg_trigger import PGTrigger
from alembic_utils.replaceable_entity import ReplaceableEntity
from typing import Iterable

_update_movie_rating_after_insert_rate = PGFunction(
  schema = 'public',
  signature = 'update_movie_rating_after_insert_rate()',
  definition = """
  RETURNS TRIGGER AS $$
    BEGIN
        UPDATE movies
        SET movie_rating_count = movie_rating_count + 1,
            movie_rating_sum = movie_rating_sum + NEW.rating
        WHERE
            id = NEW.movie_id;
    return NEW;
    END;
$$ language 'plpgsql'
  """
)


_update_movie_rating_after_update_rate = PGFunction(
  schema = 'public',
  signature = 'update_movie_rating_after_update_rate()',
  definition = """
  RETURNS TRIGGER AS $$
    BEGIN
        IF (NEW.rating <> OLD.rating) THEN
            UPDATE movies
            SET movie_rating_sum = movie_rating_sum + NEW.rating - OLD.rating
            WHERE
                id = NEW.movie_id;
        END IF;
    return NEW;
    END;
$$ language 'plpgsql'
  """
)

_update_movie_rating_after_delete_rate = PGFunction(
  schema = 'public',
  signature = 'update_movie_rating_after_delete_rate()',
  definition = """
  RETURNS TRIGGER AS $$
    BEGIN
        UPDATE movies
        SET movie_rating_count = movie_rating_count - 1,
            movie_rating_sum = movie_rating_sum - OLD.rating
        WHERE
            id = OLD.movie_id;
        
    return OLD;
    END;
$$ language 'plpgsql'
  """
)


_insert_rating_trigger = PGTrigger(
    schema = 'public',
    signature = 'insert_rating_trigger',
    on_entity = 'public.user_movie_rating',
    definition = """
        BEFORE INSERT ON public.user_movie_rating
        FOR EACH ROW 
        EXECUTE FUNCTION public.update_movie_rating_after_insert_rate();
    """
)


_update_rating_trigger = PGTrigger(
    schema = 'public',
    signature = 'update_rating_trigger',
    on_entity = 'public.user_movie_rating',
    definition = """
        BEFORE UPDATE ON public.user_movie_rating
        FOR EACH ROW 
        EXECUTE FUNCTION public.update_movie_rating_after_update_rate();
    """
)

_delete_rating_trigger = PGTrigger(
    schema = 'public',
    signature = 'delete_rating_trigger',
    on_entity = 'public.user_movie_rating',
    definition = """
        BEFORE DELETE ON public.user_movie_rating
        FOR EACH ROW 
        EXECUTE FUNCTION public.update_movie_rating_after_delete_rate();
    """
)

######################################################################
_update_movie_review_count_after_insert_review = PGFunction(
  schema = 'public',
  signature = 'update_movie_review_count_after_insert_review()',
  definition = """
  RETURNS TRIGGER AS $$
    BEGIN
        UPDATE movies
        SET movie_reviews_count = movie_reviews_count + 1
        WHERE
            id = NEW.movie_id;
    return NEW;
    END;
$$ language 'plpgsql'
  """
)

_insert_review_trigger = PGTrigger(
    schema = 'public',
    signature = 'insert_review_trigger',
    on_entity = 'public.user_review_movies',
    definition = """
        BEFORE INSERT ON public.user_review_movies
        FOR EACH ROW 
        EXECUTE FUNCTION public.update_movie_review_count_after_insert_review();
    """
)

_update_movie_review_count_after_delete_review = PGFunction(
  schema = 'public',
  signature = 'update_movie_review_count_after_delete_review()',
  definition = """
  RETURNS TRIGGER AS $$
    BEGIN
       UPDATE movies
        SET movie_reviews_count = movie_reviews_count - 1
        WHERE
            id = OLD.movie_id;
        
    return OLD;
    END;
$$ language 'plpgsql'
  """
)

_delete_review_trigger = PGTrigger(
    schema = 'public',
    signature = 'delete_review_trigger',
    on_entity = 'public.user_review_movies',
    definition = """
        BEFORE DELETE ON public.user_review_movies
        FOR EACH ROW 
        EXECUTE FUNCTION public.update_movie_review_count_after_delete_review();
    """
)



def get_all_pg_obj() -> Iterable[ReplaceableEntity]:
    for obj in globals().values():
        if isinstance(obj, ReplaceableEntity):
            yield obj
            
            