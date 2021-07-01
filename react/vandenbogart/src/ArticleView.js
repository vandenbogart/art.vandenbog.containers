import React, { useEffect } from 'react';
import { useArticleData } from './hooks/articles';

export const ArticleView = ({filename}) => {
    const articleData = useArticleData(filename);
    const id =`${filename.split('.')[0]}--view` 

    useEffect(() => {
        if (articleData.data != null) {
            document.getElementById(id).innerHTML = articleData.data.html;
        }
    }, [articleData.data])

    return (<div id={id}>
    </div>)
}