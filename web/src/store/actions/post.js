import {LOAD_POST, LOAD_PAGE_POST, SET_NO_POSTS, LOAD_RECENT_POST, VIEW_POST, CHANGE_WEB_STAS} from "../type";

export const loadPost = payload => ({
    type: LOAD_POST,
    payload: payload,
})
export const loadPagePost = payload => ({
    type: LOAD_PAGE_POST,
    payload: payload
})

export const setNOPosts = payload => ({
    type: SET_NO_POSTS,
    payload: payload
})

export const loadRecentPost = payload => ({
    type: LOAD_RECENT_POST,
    payload: payload
})

export const viewPost = payload =>({
    type:VIEW_POST,
    payload: payload
})

export const changeWebStas = payload =>({
    type:CHANGE_WEB_STAS,
    payload: payload
})