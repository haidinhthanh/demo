import align_item  from "./align_item" ;
import backgroud_color from "./backgroud_color";
import color from "./color";
import cursor from "./cursor";
import display from "./display";
import font_family from "./font_family";
import font_size from "./font_size";
import justify_content from "./justify_content";
import letter_spacing from "./letter_spacing";
import margin from "./margin";
import text_indent from "./text_indent";
import hover from "./hover";
import active from "./active";
import text_decoration from "./text_decoration";
import width from './width';
import height from "./height";
import list_style_type from "./list_style_type";
import position from "./position";
import flex_direction from "./flex_direction";
import flex from "./flex";
import float from "./float";
import flex_wrap from "./flex_wrap";
import padding from "./padding";
import font_weight from "./font_weight";
import text_align from "./text_align";
import after from "./after";
import before from "./before";
import custome from "./custome";
import border from "./border";
import zIndex from "./zIndex";
import box_shadow from "./box_shadow";
import outline from "./outline";
import background_url from "./background_url";
import text_transform from "./text_transform";
import line_height from "./line_height";
import opacity from "./opacity";
import background from "./background";
import overflow from "./overflow";
import pointer_event from "./pointer_event";
import visibility from "./visibility";
import transform from "./transform";
import transition from "./transition";
import filter from "./filter";
import min_height from "./min_height";
//show type
const d = display
const lst = list_style_type
const zi = zIndex 
const opa = opacity
const ovfl = overflow
const poev = pointer_event
const vi = visibility
const fil = filter
//border
const b = border
const bs = box_shadow
const ol = outline
//align
const ai = align_item
const jc = justify_content
const m = margin
const pad = padding
const pos = position
const flo = float

//color 
const bc = backgroud_color
const clr = color
const bgu = background_url
const bg = background
//point
const csr = cursor
const hov = hover
const act = active
const aft = after
const bef = before

//font
const ff = font_family
const fs = font_size
const fw = font_weight
const lets = letter_spacing

//text
const texi = text_indent
const texd = text_decoration
const texa = text_align
const text = text_transform
const linh = line_height
//size
const w = width
const h = height
const mih = min_height 
//flex
const fled = flex_direction
const fle = flex
const flew = flex_wrap
//custom
const cus = custome
//anim
const tsf = transform
const tsi = transition
export {
    d, lst, zi, opa, ovfl, poev, vi, fil,
    /////
    b, bs, ol,
    /////
    ai, jc, m, pad, pos, flo,
    /////
    bc, clr, bgu, bg,
    ///
    csr, hov, act, aft, bef,
    ///
    ff, fs, fw, lets,
    ///
    texi, texd, texa, text, linh,
    ///
    w, h, mih,
    ///
    fle, fled, flew,
    ///
    cus,
    //
    tsf, tsi,
}
