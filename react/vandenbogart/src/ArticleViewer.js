import React, { useEffect, useState } from 'react';

import { ArticleView } from './ArticleView';

export const ArticleViewer = ({articlesMeta, selectedArticleIndex, setSelectedArticleIndex}) => {

    const [articleLoadStatus, setArticleLoadStatus] = useState(articlesMeta.data.map((__, index) => index == selectedArticleIndex))

    const loadNextArticle = (currentArticleIndex) => {
        const newStatus = [...articleLoadStatus];
        newStatus[currentArticleIndex + 1] = true;
        setArticleLoadStatus(newStatus)
        setSelectedArticleIndex(currentArticleIndex + 1) // move to separate bound
    }

    useEffect(() => {
        document.getElementById('scrolling-article-viewer').addEventListener('scroll', (ev) => {
            const scrollPos = ev.target.scrollHeight - document.documentElement.clientHeight - ev.target.scrollTop;
            const lowerBound = 200;
            const upperBound = ev.target.scrollHeight - document.documentElement.clientHeight - 100;
            if (scrollPos < lowerBound) {
                console.log('load next article')
                loadNextArticle(selectedArticleIndex);
            }
            if (scrollPos > upperBound) {
                console.log('load previous article')
            }
        })
    }, [])

    return (
        <div id="scrolling-article-viewer" className="dashboard__right__page-display">
            {articlesMeta.data.map((article, index) => {
                if (articleLoadStatus[index]) {
                    return <ArticleView filename={articlesMeta.data[index].filename} />
                }
            })}
            
        </div>
        
    )

}