module.exports = {
    rules: {
        'header-max-length': [2, 'always', 72],
        'body-max-line-length': [2, 'always', 100],
        'footer-max-line-length': [2, 'always', 100],
        'type-empty': [2, 'never'],
        'subject-empty': [2, 'never'],
        'subject-full-stop': [2, 'never',"."],
        'footer-leading-blank': [1, 'always'],
        'body-leading-blank':[1, 'always'],
        'subject-case': [2,'always',
        ['lower-case']],
        'type-enum': [
            2,
            'always',
            ['feat',
            'fix',
            'docs',
            'refactor',
            'test',
            'perf',
            'bump',
            'chore',
            'revert',
            'build',
            'ci',
            'style']
            ],
        'type-case': [2,'always',
            ['lower-case']
        ],
        'scope-empty': [0]
    }
};
