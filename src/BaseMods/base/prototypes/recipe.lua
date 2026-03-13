local wood = data.raw.resource["wood"]
local ore = data.raw.resource["ore"]
local brick = data.raw.resource["brick"]
local cow = data.raw.resource["cow"]
local buckwheat = data.raw.resource["buckwheat"]

data:extend{
    {
        type="recipe",
        name="build-village",
        display_name="Build Village",
        result=data.raw.settlement["village"],
        ingredients={
            {
                type="ingredient",
                resource=wood,
                amount=1
            },
            {
                type="ingredient",
                resource=brick,
                amount=1
            },
            {
                type="ingredient",
                resource=cow,
                amount=1
            },
            {
                type="ingredient",
                resource=buckwheat,
                amount=1
            }
        }
    },
    {
        type="recipe",
        name="build-city",
        display_name="Build City",
        result=data.raw.settlement["city"],
        ingredients={
            {
                type="ingredient",
                resource=buckwheat,
                amount=2
            },
            {
                type="ingredient",
                resource=ore,
                amount=3
            }
        }
    }
}
