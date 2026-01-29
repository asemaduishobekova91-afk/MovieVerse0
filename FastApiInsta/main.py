from fastapi import FastAPI
from site_app.api import (profile, follow, post, post_content, city, hash_tag, post_like,
                          review_parent, review, review_like, chat, person, message, auth
                          )
import uvicorn
from site_app.admin.setup import setup_admin

site_app = FastAPI(title='Instagram')
site_app.include_router(profile.profile_router)
site_app.include_router(follow.follow_router)
site_app.include_router(post.post_router)
site_app.include_router(post_content.post_content_router)
site_app.include_router(city.city_router)
site_app.include_router(hash_tag.hash_tag_router)
site_app.include_router(post_like.post_like_router)
site_app.include_router(review_parent.review_parent_router)
site_app.include_router(review.review_router)
site_app.include_router(review_like.review_like_router)
site_app.include_router(chat.chat_router)
site_app.include_router(person.person_router)
site_app.include_router(message.message_router)
site_app.include_router(auth.auth_router)
setup_admin(site_app)


if __name__ == '__main__':
    uvicorn.run(site_app, host='127.0.0.1', port=8002
                )