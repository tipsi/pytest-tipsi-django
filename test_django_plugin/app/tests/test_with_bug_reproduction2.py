from datetime import datetime

import pytest
from django.contrib.auth.models import User
from django.test.utils import CaptureQueriesContext


# issue: module fixture must exist,
# if not , these case raise  django.db.utils.OperationalError: (1305, 'SAVEPOINT s4737629504_x65 does not exist')
# remove below module fixture  it should be fail
# @pytest.fixture(scope='module', autouse=True)
# def this_is_module_fixture(module_fixture):
#     pass


@pytest.fixture(scope='function', autouse=False)
def this_is_function_fixture():
    return User.objects.create(username='this user available in function level')


@pytest.mark.django_db
def test_check_raise_savepiont_does_not_exist(request):
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_check_raise_savepiont_does_not_exist2():
    User.objects.create(username='this user available only in this testcase')

    assert 'this user available only in this testcase' in User.objects.all().values_list('username', flat=True)
    assert User.objects.count() == 1


@pytest.mark.usefixtures('this_is_function_fixture')
@pytest.mark.django_db
def test_check_raise_savepiont_does_not_exist3():
    assert 'this user available in function level' in User.objects.all().values_list('username', flat=True)
    assert User.objects.count() == 1


@pytest.mark.parametrize(
    argnames='parametrize_idx_aaa',
    argvalues=(1, 2, 3, 4,)
)
@pytest.mark.django_db
def test_check_raise_savepiont_does_not_exist4(parametrize_idx_aaa):
    User.objects.create(username='username_{}'.format(parametrize_idx_aaa))

    # assert 'this user available in module level' in User.objects.all().values_list('username', flat=True)
    assert 'username_{}'.format(parametrize_idx_aaa) in User.objects.all().values_list('username', flat=True)
    assert User.objects.count() == 1


@pytest.mark.parametrize(
    argnames='parametrize_idx_aaa,expected_value',
    argvalues=((1, 1), (2, 1), (3, 1), (4, datetime(2019, 10, 11)),)
)
@pytest.mark.django_db
def test_check_raise_savepiont_does_not_exist401(request, parametrize_idx_aaa, expected_value):
    print('\n\n\n--check fixturenames---{}----------\n\n\n'.format(request.fixturenames))

    User.objects.create(username='username_{}'.format(parametrize_idx_aaa))

    assert 'username_{}'.format(parametrize_idx_aaa) in User.objects.all().values_list('username', flat=True)
    assert User.objects.count() == 1


@pytest.mark.parametrize(
    argnames='parametrize_idx_aaa,expected_value',
    argvalues=((1, 1), (2, 1), (3, 1), (4, datetime(2019, 10, 11)),)
)
@pytest.mark.django_db
def test_check_raise_savepiont_does_not_exist402(parametrize_idx_aaa, expected_value):
    User.objects.create(username='username_{}'.format(parametrize_idx_aaa))

    assert 'username_{}'.format(parametrize_idx_aaa) in User.objects.all().values_list('username', flat=True)
    assert User.objects.count() == 1


@pytest.mark.parametrize(
    argnames='parametrize_idx_aaa,expected_value',
    argvalues=((1, ValueError), (2, ValueError), (3, ValueError), (4, ValueError),)
)
@pytest.mark.django_db
def test_check_raise_savepiont_does_not_exist402(parametrize_idx_aaa, expected_value):
    User.objects.create(username='username_{}'.format(parametrize_idx_aaa))
    try:
        raise ValueError
    except ValueError:
        pass
    assert 'username_{}'.format(parametrize_idx_aaa) in User.objects.all().values_list('username', flat=True)
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_check_raise_savepiont_does_not_exist5():
    from django.db import connection
    with CaptureQueriesContext(connection) as expected_num_queries:
        User.objects.create(username='username_123')

    # with CaptureQueriesContext(connection) as expected_num_queries2:
    #     APIClient().get(path='www.naver.com')

    assert len(expected_num_queries.captured_queries) == 1
    assert User.objects.count() == 1