# tests for the rivers app workflows

import pytest
import bs4

from django.urls import reverse
from river.models import River, RiverMembership
from userauth.util import user_to_slug

def test_river_view(client, test_river):
    rivers_page = client.get(reverse('spring', args=[test_river.area.name]))
    assert test_river.name in rivers_page.content.decode('utf-8')
    single_river_view = client.get(reverse('view_river', args=[test_river.slug]))
    assert test_river.description in single_river_view.content.decode('utf-8')

def test_project_edit(client, test_user, test_river):
    RiverMembership.objects.create(user = test_user, river = test_river, starter = True)
    attempt_logged_out = client.get(reverse('edit_river', args=[test_river.slug]))
    assert attempt_logged_out.status_code == 302
    client.force_login(test_user)
    attempt_logged_in = client.get(reverse('edit_river', args=[test_river.slug]))
    assert attempt_logged_in.status_code == 200
    client.post(reverse('edit_river', args=[test_river.slug]), {'name': 'new edited name',
                                                                  'description': 'new edited description'})
    assert River.objects.get(pk=test_river.id).name == 'new edited name'

def test_project_membership(client, test_user, other_test_user, test_river):
    # non-starter members
    client.force_login(test_user)
    river_page = client.get(reverse('view_river', args=[test_river.slug]))
    river_page_html = bs4.BeautifulSoup(river_page.content, features='html5lib')
    join_button = river_page_html.find('button')
    assert join_button.text == 'join river'
    client.post(reverse('view_river', args=[test_river.slug]), {'action': 'join'})
    assert len(RiverMembership.objects.filter(user=test_user, river=test_river)) == 1
    river_page_member = client.get(reverse('view_river', args=[test_river.slug]))
    river_page_member_html = bs4.BeautifulSoup(river_page_member.content, features='html5lib')
    leave_button = river_page_member_html.find('button')
    assert leave_button.text == 'leave river'
    client.post(reverse('view_river', args=[test_river.slug]), {'action': 'leave'})
    assert len(RiverMembership.objects.filter(user=test_user, river=test_river)) == 0
    # chat part no longer applicable now river chats are more complex, needs to be replaced once the new chat system is in place
    #chat_page = client.get(reverse('river_chat', args=[test_river.slug]))
    #assert test_user.display_name + ' left this river' in str(chat_page.content)
    # owners
    ownership = RiverMembership(user=test_user, river=test_river, owner=True)
    other_ownership = RiverMembership(user=other_test_user, river=test_river, owner=True)
    ownership.save()
    other_ownership.save()
    river_page_owner = client.get(reverse('view_river', args=[test_river.slug]))
    river_page_owner_html = bs4.BeautifulSoup(river_page_owner.content, features='html5lib')
    edit_link = river_page_owner_html.find_all('a')[0]
    assert edit_link.text == 'Edit River'
    edit_page = client.get(reverse('edit_river', args=[test_river.slug]))
    edit_page_html = bs4.BeautifulSoup(edit_page.content, features='html5lib')
    abdicate_button = edit_page_html.find('button', attrs={'name': 'abdicate'})
    assert abdicate_button.text == 'Rescind Starter Status'
    client.post(reverse('edit_river', args=[test_river.slug]), {'name': test_river.name,
                                                                    'description': test_river.description,
                                                                    'abdicate': 'abdicate'})
    assert RiverMembership.objects.get(user=test_user, river=test_river).starter == False
    # chat part no longer applicable now river chats are more complex, needs to be replaced once the new chat system is in place
    #chat_page = client.get(reverse('river_chat', args=[test_river.slug]))
    #assert test_user.display_name + ' is no longer an starter of this river' in str(chat_page.content)
    client.force_login(other_test_user)
    edit_page_last_owner = client.get(reverse('edit_river', args=[test_river.slug]))
    edit_page_last_owner_html = bs4.BeautifulSoup(edit_page_last_owner.content, features='html5lib')
    assert 1 == len([p for p in edit_page_last_owner_html.find_all('p') if p.text == 'As you are the only starter of this river, you cannot rescind ownership'])
    client.post(reverse('edit_river', args=[test_river.slug]), {'name': test_river.name,
                                                                  'description': test_river.description,
                                                                  'abdicate': 'abdicate'}) # should be rejected
    assert RiverMembership.objects.get(user=other_test_user, river=test_river).starter == True

def test_project_management(client, test_user, other_test_user, test_river):
    membership = RiverMembership(user=test_user, river=test_river, starter=True)
    other_membership = RiverMembership(user=other_test_user, river=test_river, starter=False)
    membership.save()
    other_membership.save()
    client.force_login(test_user)
    management_page = client.get(reverse('manage_river', args=[test_river.slug]))
    management_page_html = bs4.BeautifulSoup(management_page.content, features='html5lib')
    members = management_page_html.find('table', attrs={'id':'members'}).tbody.find_all('tr')[1:] # drop the headings row
    assert len(members) == 2
    client.post(reverse('manage_river', args=[test_river.slug]), {'membership': other_membership.id,
                                                                      'action': 'offer_championship'})
    client.force_login(other_test_user)
    user_chat = client.get(reverse('user_chat', args=[user_to_slug(test_user)]))
    user_chat_html = bs4.BeautifulSoup(user_chat.content, features='html5lib')
    action_id = user_chat_html.find('input', attrs={'type':'hidden', 'name':'action_id'})['value']
    client.post(reverse('do_action'), {'action_id': action_id, 'choice': 'invoke'})
    assert RiverMembership.objects.get(user=other_test_user, river=test_river).champion

    client.post(reverse('manage_river', args=[test_river.slug]), {'membership': other_membership.id,
                                                                      'action': 'remove_championship'}) # should be rejected
    assert RiverMembership.objects.get(user=other_test_user, river=test_river).champion
    client.force_login(test_user)
    client.post(reverse('manage_river', args=[test_river.slug]), {'membership': other_membership.id,
                                                                      'action': 'remove_championship'}) # should be accepted
    assert not RiverMembership.objects.get(user=other_test_user, river=test_river).champion


def test_river_stages(test_river):
    test_river.start_envision()
    assert River.objects.get(id = test_river.id).envision_stage is not None
    test_river.start_plan()
    assert River.objects.get(id = test_river.id).plan_stage is not None
    test_river.start_act()
    assert River.objects.get(id = test_river.id).act_stage is not None
    test_river.start_reflect()
    assert River.objects.get(id = test_river.id).reflect_stage is not None
    








