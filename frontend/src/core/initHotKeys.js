/*
 * @Author: 秦少卫
 * @Date: 2022-12-07 23:50:05
 * @LastEditors: 秦少卫
 * @LastEditTime: 2023-01-07 02:06:16
 * @Description: 快捷键功能
 */

import hotkeys from 'hotkeys-js'
import { cloneDeep } from 'lodash-es'
import { v4 as uuid } from 'uuid'
import { ElMessage } from 'element-plus'

const keyNames = {
    lrdu: 'left,right,down,up', // 左右上下
    backspace: 'backspace', // backspace键盘
    ctrlz: 'ctrl+z',
    ctrlc: 'ctrl+c',
    ctrlv: 'ctrl+v'
}

function initHotkeys(canvas) {
    // 删除快捷键
    hotkeys(keyNames.backspace, function () {
        const activeObject = canvas.getActiveObjects()
        if (activeObject) {
            activeObject.map(item => canvas.remove(item))
            canvas.requestRenderAll()
            canvas.discardActiveObject()
        }
    })

    // 移动快捷键
    hotkeys(keyNames.lrdu, (event, handler) => {
        const activeObject = canvas.getActiveObject()
        if (activeObject) {
            switch (handler.key) {
                case 'left':
                    activeObject.set('left', activeObject.left - 1)
                    break;
                case 'right':
                    activeObject.set('left', activeObject.left + 1)
                    break;
                case 'down':
                    activeObject.set('top', activeObject.top + 1)
                    break;
                case 'up':
                    activeObject.set('top', activeObject.top - 1)
                    break;
                default:
            }
            canvas.renderAll()
        }
    })

    // 复制粘贴
    copyElement(canvas)

}


function copyElement(canvas) {
    let copyEl = null

    // 复制
    hotkeys(keyNames.ctrlc, (event, handler) => {
        const activeObject = canvas.getActiveObjects()
        if (activeObject.length === 0) return
        copyEl = cloneDeep(activeObject[0])
        if (copyEl.left === activeObject[0].left) {
            copyEl.left += 10
            copyEl.top += 10
        }
        // ElMessage.success('复制成功')
    })
    // 粘贴
    hotkeys(keyNames.ctrlv, (event, handler) => {
        if (!copyEl) return ElMessage.warning('暂无复制内容')
        const myCopyEl = cloneDeep(copyEl)
        myCopyEl.id = uuid()
        copyEl.left += 10
        copyEl.top += 10
        canvas.add(myCopyEl)
        canvas.setActiveObject(myCopyEl)
    })
}

export default initHotkeys
export { keyNames, hotkeys }