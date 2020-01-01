import {LOAD_POST, LOAD_PAGE_POST, SET_NO_POSTS, LOAD_RECENT_POST, VIEW_POST, CHANGE_WEB_STAS} from "../type";
import { hash} from "../../assets/hash_config";


export const loadPost = (state = {posts:[]}, {type, payload})=>{
    switch(type){
        case LOAD_POST:{
            return {
                ...state,
                posts: payload.posts
            }
        }
        default:
            return state
    }
}

export const pagePost = (state = {pagePosts:[], noPosts: 0}, {type,payload})=>{
    switch(type){
        case LOAD_PAGE_POST:{
            return {
                ...state,
                pagePosts: payload.pagePosts
            }
        }
        case SET_NO_POSTS:{
            return {
                ...state,
                noPosts: payload.noPosts
            }
        }
        default:
            return state
    }
}


export const recentPost = (state = {recentPosts:[]}, {type,payload})=>{
    switch(type){
        case LOAD_RECENT_POST:{
            return {
                ...state,
                recentPosts : payload.recentPosts
            }
        }
        default:
            return state
    }
}


export const viewPost = (state = {post:{}}, {type,payload})=>{
    switch(type){
        case VIEW_POST:{
            return {
                ...state,
                post : payload.post
            }
        }
        default:
            return state
    }
}

export const web = (state = {isFirstOpen: true}, {type,payload})=>{
    switch(type){
        case CHANGE_WEB_STAS:{
            return {
                isFirstOpen : payload.isFirstOpen
            }
        }
        default:
            return state
    }
}