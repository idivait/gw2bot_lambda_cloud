const { performance } = require('perf_hooks');


/**
 * @fileOverview A sample script to demonstrate parallel collection runs using async.
 */

var path = require('path'), // ensures that the path is consistent, regardless of where the script is run from

    async = require('async'), // https://npmjs.org/package/async
    newman = require('newman'), // change to require('newman'), if using outside this repository

    /**
     * A set of collection run options for the paralle collection runs. For demonstrative purposes in this script, an
     * identical set of options has been used. However, different options can be used, so as to actually run different
     * collections, with their corresponding run options in parallel.
     *
     * @type {Object}
     */
    options = {
        collection: path.join(__dirname, 'lambdatests.postman_collection.json')
    },

    /**
     * A collection runner function that runs a collection for a pre-determined options object.
     *
     * @param {Function} done - A callback function that marks the end of the current collection run, when called.
     */
    parallelCollectionRun = function (n, done) {
        newman.run(options, done);
        return "test"
    };

t1 = performance.now()
async.timesLimit(6000, 50, parallelCollectionRun,

/**
 * The
 *
 * @param {?Error} err - An Error instance / null that determines whether or not the parallel collection run
 * succeeded.
 * @param {Array} results - An array of collection run summary objects.
 */
function (err, results) {
    err && console.error(err);
    t2 = performance.now()
    m = ( t2 - t1 ) / 60000
    s = (m - m.toFixed(0)) * 60
    ms = (s - s.toFixed(0)) * 1000
    console.info(`\nTime to Complete: ${m.toFixed(0)}m ${s}s`)

    total = {
        'collections' : 0,
        'failures' : [],
        'tests' : {
            'run': 0,
            'fail': 0
        }
    }

    results.forEach(function (result) {
        total.collections++;
        if(result.run.failures.length) total.failures.push(result.run.failures);
        total.tests.run += result.run.stats.assertions.total;
        total.tests.fail += result.run.stats.assertions.failed;
        if(result.run.failures.length) console.info(JSON.stringify(result.run.failures, null, 2));
    });

    console.info(
`
${total.collections} Collections Tested:
    Failures: 
    ${JSON.stringify(total.failures, null, 2)}
    Tests Run: ${total.tests.run}
    Tests Failed: ${total.tests.fail}
`
    )
});
